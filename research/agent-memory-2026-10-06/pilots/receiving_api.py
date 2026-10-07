#!/usr/bin/env python3
"""Explicit finite NVIDIA text-only dispatch for fictional receiving exchange.

No agent, source database, private session, tool execution or native memory is
started. Provider schema decoding is selectable; local receiving criteria stay
unchanged. A failed/unknown dispatch is preserved and stops this finite run.
"""
import argparse
import json
from pathlib import Path
import time
import urllib.error
import urllib.request

import receiving_exchange as exchange

ENDPOINT = 'https://integrate.api.nvidia.com/v1/chat/completions'


def parameters(request, output_limit, provider_format):
    if (request.get('format') != 'hmk-fictional-receiving-request/v1'
            or not request.get('model', '').startswith('nvidia/')
            or request.get('fresh_context') is not True
            or request.get('tools_allowed') is not False
            or request.get('native_memory_allowed') is not False):
        raise ValueError('only fresh, tool-free fictional NVIDIA requests are supported')
    if provider_format not in {'plain', 'schema'} or not 1 <= output_limit <= 32768:
        raise ValueError('invalid explicit output/format setting')
    messages = request['messages']
    if (not isinstance(messages, list) or not messages
            or any(set(m) != {'role', 'content'} or not isinstance(m['content'], str)
                   or m['role'] not in {'system', 'user', 'assistant'} for m in messages)):
        raise ValueError('messages must contain only supplied textual roles/content')
    # The same explicit output instruction is supplied in either decoder mode.
    # This is a disclosed provider adapter; no rubric or outside source is added.
    messages = [dict(messages[0], content=messages[0]['content'] +
        '\nReturn only JSON conforming to this output schema. This constrains '
        'syntax, not evidence or truth:\n' + json.dumps(request['response_schema'])),
        *messages[1:]]
    value = dict(model=request['model'], messages=messages, temperature=0,
                 reasoning_effort=request['reasoning_effort'], max_tokens=output_limit)
    if provider_format == 'schema':
        value['response_format'] = dict(type='json_schema', json_schema=dict(
            name='fictional_receiving', strict=True, schema=request['response_schema']))
    # Unsupported reasoning_budget is deliberately absent, not a local limit
    # change. Both arms use these same frozen settings.
    return value


def dispatch(request_path, root, output_limit=12000, provider_format='plain',
             opener=urllib.request.urlopen, timeout=300, retry_failed=False):
    request = json.loads(request_path.read_text())
    key_hash = exchange.pilot.digest(request)
    if request_path.stem != key_hash:
        raise ValueError('prepared request filename/hash mismatch')
    payload = parameters(request, output_limit, provider_format)
    receipt_path = root/'dispatches'/(key_hash+'.json')
    response_path = root/'responses'/(key_hash+'.json')
    if not 1 <= timeout <= 600:
        raise ValueError('request transport timeout must be between 1 and 600 seconds')
    if response_path.exists():
        raise ValueError('dispatch already observed or unresolved; preserve it instead of repeating')
    attempt = 1
    if receipt_path.exists():
        previous = json.loads(receipt_path.read_text())
        if (not retry_failed or previous['state'] != 'failed'
                or previous['parameters'] != payload):
            raise ValueError('dispatch already observed or unresolved; preserve it instead of repeating')
        attempt = 2
        receipt_path = root/'dispatches'/(key_hash+'-retry1.json')
        if receipt_path.exists():
            raise ValueError('one explicit retry was already observed; preserve both attempts')
    key = exchange.pilot.configuration.read_env_key('NVIDIA_API_KEY')
    if not key:
        raise ValueError('configured NVIDIA inference key required')
    receipt_path.parent.mkdir(exist_ok=True)
    receipt = dict(request_sha256=key_hash, provider=ENDPOINT,
        parameters=payload, parameters_sha256=exchange.pilot.digest(payload),
        fresh_context_basis='one stateless text-only HTTP request with only these messages',
        native_memory_basis='no native harness is invoked',
        state='started', usage=None, attempt=attempt, transport_timeout_seconds=timeout,
        retry_basis='explicit same-parameters retry after a failed client request; earlier server work/usage unknown'
            if attempt == 2 else None)
    exchange.pilot.save(receipt_path, receipt)
    started = time.monotonic()
    call = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(),
        headers={'Authorization':'Bearer '+key, 'Content-Type':'application/json'})
    try:
        with opener(call, timeout=timeout) as response:
            result = json.load(response)
            receipt['http_status'] = response.status
        choice = result['choices'][0]
        message = choice['message']
        # Retain final output and usage, not provider reasoning or credentials.
        receipt.update(state='completed', response_id=result.get('id'),
            response_model=result.get('model'), usage=result.get('usage'),
            finish_reason=choice.get('finish_reason'), content=message.get('content'),
            tool_calls_observed=message.get('tool_calls') or [])
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError, IndexError) as error:
        receipt.update(state='failed', error_type=type(error).__name__)
        if isinstance(error, urllib.error.HTTPError):receipt['http_status'] = error.code
        raise
    finally:
        receipt['seconds'] = time.monotonic()-started
        exchange.pilot.save(receipt_path, receipt)
    if receipt['tool_calls_observed'] or not isinstance(receipt['content'], str):
        raise ValueError('unexpected tool request or missing final text; preserve actual receipt')
    response_path.parent.mkdir(exist_ok=True)
    exchange.pilot.save(response_path, dict(request_sha256=key_hash,
        requested_model=request['model'], response_model=receipt['response_model'],
        fresh_context=True, tool_calls_observed=[], dispatch_receipt=str(receipt_path),
        usage=receipt['usage'], seconds=receipt['seconds'], content=receipt['content'],
        finish_reason=receipt['finish_reason']))
    return receipt_path


def run(packet_root, out, model, effort, output_limit, provider_format, max_calls, resume=False,
        timeout=300, retry_failed=False, adopt_transport=False):
    if not model.startswith('nvidia/') or not 1 <= max_calls <= 400:
        raise ValueError('an explicit NVIDIA model and finite call bound are required')
    if (provider_format not in {'plain', 'schema'} or not 1 <= output_limit <= 32768
            or not 1 <= timeout <= 600):
        raise ValueError('invalid explicit output/format setting')
    settings = dict(model=model, effort=effort, output_limit=output_limit,
        provider_format=provider_format, endpoint=ENDPOINT,
        dispatcher_sha256=exchange.checksum(Path(__file__)), qualification=False,
        timeout_seconds=timeout, max_attempts_per_request=2)
    conditions = out/'provider-conditions.json'
    if resume:
        prior = json.loads(conditions.read_text())
        if prior != settings:
            semantic = ('model','effort','output_limit','provider_format','endpoint','qualification')
            if not adopt_transport or any(prior.get(k) != settings[k] for k in semantic):
                raise ValueError('provider settings changed; preserve pending comparison')
            history_path = out/'provider-conditions-history.json'
            history = json.loads(history_path.read_text()) if history_path.exists() else []
            history.append(dict(previous=prior, adopted=settings,
                scope='explicit transport-only adoption; model messages/schema/evidence and receiving procedure remain frozen'))
            exchange.pilot.save(history_path,history)
            exchange.pilot.save(conditions,settings)
    elif out.exists():
        raise ValueError('new receiving run must not overwrite existing work')
    state = exchange.receive(packet_root, out, model, effort, resume=resume)
    if not resume:exchange.pilot.save(conditions, settings)
    for index in range(max_calls+1):
        exchange.pilot.save(out/'dispatch-state.json', state)
        if state['state'] != 'prepared' or index == max_calls:
            return dict(state, new_dispatches=index)
        path = dispatch(Path(state['request']), out, output_limit, provider_format,
                        timeout=timeout, retry_failed=retry_failed)
        print(json.dumps(dict(dispatch=str(path), call=index+1,
                              completed_candidates=state['completed_candidates'])), flush=True)
        state = exchange.receive(packet_root, out, model, effort, resume=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packets', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--effort', default='high')
    parser.add_argument('--output-limit', type=int, default=12000)
    parser.add_argument('--provider-format', choices=['plain', 'schema'], required=True)
    parser.add_argument('--max-calls', type=int, required=True)
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--timeout-seconds', type=int, default=300)
    parser.add_argument('--retry-failed', action='store_true',
        help='Permit one recorded same-parameters retry of a failed request; never repeat a completed or started request')
    parser.add_argument('--adopt-transport', action='store_true',
        help='Explicitly preserve old transport conditions while adopting a dispatcher/timeout change; model settings must match')
    args = parser.parse_args()
    print(json.dumps(run(args.packets, args.out, args.model, args.effort,
        args.output_limit, args.provider_format, args.max_calls, args.resume,
        args.timeout_seconds, args.retry_failed, args.adopt_transport)))


if __name__ == '__main__':main()
