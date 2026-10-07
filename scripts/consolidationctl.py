#!/usr/bin/env python3
"""Preview and apply finite, evidence-linked dream proposals; no model or timer."""
from __future__ import annotations

import argparse
import json

import memoryctl as mc
from capturectl import CaptureLedger, digest


FIELDS = ('id','record_uid','revision','title','raw','spr','engram_type','event_ts','source_metadata_json')


def snapshot(row):
    return {key: row[key] for key in FIELDS}


def preview(chapter_ids, memory=mc):
    """Full selected episode input, without a hidden per-source text cutoff."""
    if not chapter_ids or len(set(chapter_ids)) != len(chapter_ids):
        raise ValueError('select a nonempty finite set of distinct episodes')
    supports = []
    for cid in chapter_ids:
        row = memory._read_chapter(cid)
        if row['engram_type'] != 'episodic' or row['origin']['kind'] == 'daimon-projection':
            raise ValueError('generic dream input must be native episodes; protected sources keep their owner contract')
        supports.append(snapshot(row))
    return {'schema': 'hmk-dream-preview/v1', 'supports': supports,
            'fingerprint': digest(supports), 'input_count': len(supports),
            'independence': 'Input count does not establish independent corroboration.'}


def apply(manifest, decision, *, stream_id, sequence, event_id, selection_version, memory=mc, _fault_hook=None):
    """Apply a reviewed proposal; evidence and writes share one transaction.

    A structurally valid inference is not evidence that its prose is true.
    The selecting body must inspect all supplied inputs, preserve uncertainty
    and evaluate the output against the capture/recall pilot contract.
    """
    if (not isinstance(manifest, dict) or manifest.get('schema') != 'hmk-dream-preview/v1'
            or not isinstance(manifest.get('supports'), list) or not manifest['supports']
            or manifest.get('fingerprint') != digest(manifest['supports'])):
        raise ValueError('invalid evidence manifest')
    supports = manifest['supports']
    ids = [entry['id'] for entry in supports]
    if len(set(ids)) != len(ids):
        raise ValueError('a repeated episode does not provide independent corroboration')
    if decision.get('outcome') != 'applied' or not decision.get('records'):
        raise ValueError('consolidation requires selected account/learning proposals')
    records = []
    for item in decision['records']:
        record = dict(item)
        if record.get('engram_type', 'semantic') not in {'semantic','procedural'}:
            raise ValueError('consolidation cannot create or replace lived episodes')
        if record.get('operation') == 'add' and record.get('shelf') not in {'library','plans','mc-social','mc-skills','mc-places'}:
            raise ValueError('generic dream proposals target knowledge/procedure shelves')
        metadata = dict(record.get('metadata') or {})
        if metadata.get('mode', 'inferred') not in {'inferred','generated'}:
            raise ValueError('consolidation is inferred/generated, not an independent observation')
        metadata.setdefault('mode', 'inferred')
        metadata['evidence'] = [f"mem:{entry['record_uid']}@{entry['revision']}" for entry in supports]
        records.append(dict(record, metadata=metadata, engram_type=record.get('engram_type','semantic')))
    links = list(decision.get('links', []))
    for record in records:
        links.extend({'source': record['key'], 'target': cid, 'link_type': 'supported-by',
                      'note': 'Derived account; the source episode is not superseded.'} for cid in ids)
    proposal = dict(decision, records=records, links=links, selection_version=selection_version)
    ledger = CaptureLedger(memory)
    event = {'stream_id': stream_id, 'sequence': sequence, 'event_id': event_id,
             'source_version': manifest['fingerprint'],
             'content': json.dumps({'manifest': manifest, 'proposal': proposal}, ensure_ascii=False),
             'metadata': {'mode': 'inferred', 'evidence': [f"mem:{entry['record_uid']}@{entry['revision']}" for entry in supports]}}
    staged = ledger.stage(event)

    def validate(con):
        for entry in supports:
            row = con.execute('SELECT * FROM chapters WHERE id=?', (entry['id'],)).fetchone()
            if not row or snapshot(row) != entry or row['engram_type'] != 'episodic':
                raise ValueError('support changed since preview; inspect a fresh manifest')
            if con.execute('SELECT 1 FROM daimon_projections WHERE chapter_id=?', (entry['id'],)).fetchone():
                raise ValueError('protected source cannot enter generic consolidation')
        for record in records:
            if record.get('operation') == 'update':
                target = con.execute('SELECT c.engram_type,s.name FROM chapters c JOIN books b ON b.id=c.book_id JOIN shelves s ON s.id=b.shelf_id WHERE c.id=?', (record.get('chapter_id'),)).fetchone()
                if not target or target[0] == 'episodic' or target[1] not in {'library','plans','mc-social','mc-skills','mc-places'}:
                    raise ValueError('consolidation cannot overwrite episodes/identity')

    return ledger.assess(staged['event_key'], proposal, _validator=validate, _fault_hook=_fault_hook)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    inspect = sub.add_parser('preview'); inspect.add_argument('--ids', nargs='+', type=int, required=True)
    commit = sub.add_parser('apply'); commit.add_argument('--manifest', required=True); commit.add_argument('--proposal', required=True)
    commit.add_argument('--stream', required=True); commit.add_argument('--sequence', type=int, required=True)
    commit.add_argument('--event-id', required=True); commit.add_argument('--selection-version', required=True)
    args = parser.parse_args()
    if args.action == 'preview':
        result = preview(args.ids)
    else:
        with open(args.manifest, encoding='utf-8') as handle:
            manifest = json.load(handle)
        with open(args.proposal, encoding='utf-8') as handle:
            proposal = json.load(handle)
        result = apply(manifest, proposal, stream_id=args.stream, sequence=args.sequence,
                       event_id=args.event_id, selection_version=args.selection_version)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
