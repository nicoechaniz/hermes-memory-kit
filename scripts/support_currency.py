"""Native source-version currency, including dependent accounts; not truth proof."""
import json
import re


def references(metadata, source_kind=None):
    refs = []
    for value in metadata.get('evidence', []):
        match = re.fullmatch(r'mem:([0-9a-f-]{36})@(\d+)', value)
        if match:
            refs.append((match[1], int(match[2])))
    if source_kind == 'auto' and metadata.get('source_version', '').isdigit():
        refs.append((metadata.get('source_event_id', ''), int(metadata['source_version'])))
    return list(dict.fromkeys(refs))


def check(con, refs):
    """Evaluate the reachable revision graph once, without recursive depth limits.

    An unchanged account can still depend on a changed original. Cycles are
    unresolved, never corroboration. The caller owns the read/write transaction.
    """
    nodes, states = {}, {}
    for root in dict.fromkeys(refs):
        stack, active = [(root, False)], set()
        while stack:
            key, leaving = stack.pop()
            if leaving:
                active.discard(key)
                if key not in states:
                    states[key] = ('current' if all(states[child] == 'current'
                                   for child in nodes[key]) else 'needs_reconciliation')
                continue
            if key in states:
                continue
            if key in active:
                states[key] = 'cyclic'
                continue
            uid, revision = key
            row = con.execute('SELECT c.revision,c.source_metadata_json,b.source_kind '
                              'FROM chapters c JOIN books b ON b.id=c.book_id '
                              'WHERE c.record_uid=?', (uid,)).fetchone()
            if not row or row['revision'] != revision:
                states[key] = 'missing' if not row else 'changed'
                continue
            children = references(json.loads(row['source_metadata_json'] or '{}'), row['source_kind'])
            nodes[key] = children
            active.add(key)
            stack.append((key, True))
            stack.extend((child, False) for child in reversed(children))
    result = []
    for uid, revision in dict.fromkeys(refs):
        root = (uid, revision)
        entry = dict(record_uid=uid, revision=revision, status=states[root])
        if entry['status'] == 'needs_reconciliation':
            seen, pending, failures = set(), list(nodes[root]), []
            while pending:
                key = pending.pop()
                if key in seen:
                    continue
                seen.add(key)
                if states[key] in {'changed','missing','cyclic'}:
                    failures.append(dict(record_uid=key[0], revision=key[1], status=states[key]))
                pending.extend(nodes.get(key, []))
            entry['dependencies'] = failures
        result.append(entry)
    return result
