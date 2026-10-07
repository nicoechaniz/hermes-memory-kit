#!/usr/bin/env python3
"""One explicit DeepSeek generation diagnostic, not a consolidation run.

Consumes a prepared fictional request. No retrieval, reviewer, retry, agent or
production configuration is invoked. Credentials are passed in memory by the
caller; the receipt keeps final text and usage but never reasoning or secrets.
"""
import json
from pathlib import Path
import time
import urllib.error
import urllib.request

import receiving_exchange as exchange

ENDPOINT = 'https://api.deepseek.com/v1/chat/completions'


def parameters(request):
    if (request.get('format') != 'hmk-fictional-receiving-request/v1'
            or request.get('model') != 'deepseek-flash'
            or request.get('phase') != 'narrative_generation'
            or request.get('reasoning_effort') != 'low'
            or request.get('fresh_context') is not True
            or request.get('tools_allowed') is not False
            or request.get('native_memory_allowed') is not False):
        raise ValueError('only prepared fictional DeepSeek Flash low generation is supported')
    messages = request['messages']
    if (not isinstance(messages, list) or not messages
            or messages[0].get('role') != 'system'
            or any(set(m) != {'role', 'content'} or not isinstance(m['content'], str)
                   or m['role'] not in {'system', 'user'} for m in messages)):
        raise ValueError('only supplied system/user text is supported')
    messages = [dict(messages[0], content=messages[0]['content'] +
        '\nReturn only JSON conforming to this output schema. This constrains '
        'syntax, not evidence or truth:\n' + json.dumps(request['response_schema'])),
        *messages[1:]]
    # DeepSeek documents JSON-object mode, not this schema as strict decoding.
    # Temperature is omitted: thinking mode ignores it. No reasoning budget is
    # imposed; max_tokens bounds the entire provider output, including thinking.
    return dict(model='deepseek-flash', messages=messages,
                thinking={'type': 'enabled'}, reasoning_effort='low',
                max_tokens=12000, response_format={'type': 'json_object'})


def dispatch(request_path, root, api_key, opener=urllib.request.urlopen):
    request_path, root = Path(request_path), Path(root)
    request = json.loads(request_path.read_text())
    key_hash = exchange.pilot.digest(request)
    if request_path.stem != key_hash:
        raise ValueError('request filename/hash mismatch')
    payload = parameters(request)
    if not isinstance(api_key, str) or not api_key.strip():
        raise ValueError('explicit configured DeepSeek credential required')
    receipt_path = root/'dispatches'/(key_hash+'.json')
    response_path = root/'responses'/(key_hash+'.json')
    if receipt_path.exists() or response_path.exists():
        raise ValueError('preserve observed or unresolved dispatch; no implicit retry')
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt = dict(request_sha256=key_hash, provider=ENDPOINT,
        parameters=payload, parameters_sha256=exchange.pilot.digest(payload),
        fresh_context_basis='one stateless text-only HTTP request with only these messages',
        native_memory_basis='no native harness is invoked',
        state='started', usage=None, qualification=False, transport_timeout_seconds=300)
    exchange.pilot.save(receipt_path, receipt)
    started = time.monotonic()
    call = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
        headers={'Authorization': 'Bearer '+api_key, 'Content-Type': 'application/json'})
    try:
        with opener(call, timeout=300) as response:
            result = json.load(response)
            receipt['http_status'] = response.status
        choice = result['choices'][0]
        message = choice['message']
        receipt.update(state='completed', response_id=result.get('id'),
            response_model=result.get('model'), usage=result.get('usage'),
            finish_reason=choice.get('finish_reason'), content=message.get('content'),
            tool_calls_observed=message.get('tool_calls') or [])
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, IndexError) as error:
        receipt.update(state='failed', error_type=type(error).__name__)
        if isinstance(error, urllib.error.HTTPError):
            receipt['http_status'] = error.code
        raise
    finally:
        receipt['seconds'] = time.monotonic()-started
        exchange.pilot.save(receipt_path, receipt)
    if receipt['tool_calls_observed'] or not isinstance(receipt['content'], str):
        raise ValueError('unexpected tool request or missing final text; preserve receipt')
    response_path.parent.mkdir(exist_ok=True)
    exchange.pilot.save(response_path, dict(request_sha256=key_hash,
        requested_model=request['model'], response_model=receipt['response_model'],
        fresh_context=True, tool_calls_observed=[], dispatch_receipt=str(receipt_path),
        usage=receipt['usage'], seconds=receipt['seconds'], content=receipt['content'],
        finish_reason=receipt['finish_reason']))
    return receipt_path
