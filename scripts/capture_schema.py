"""Closed structural schema for explicit selection proposals; not a truth gate."""
import native_records

RECORD_FIELDS = frozenset({'key','operation','shelf','title','raw','summary','tags',
                          'importance','engram_type','event_ts','actor','location',
                          'metadata','chapter_id','expected_revision'})


def decision_schema():
    metadata = {key: {'type': 'string'} for key in sorted(native_records.SOURCE_FIELDS)}
    metadata.update(mode={'enum': sorted(native_records.MODES)},
                    reported_at={'type': 'integer'}, event_end_ts={'type': 'integer'},
                    evidence={'type': 'array', 'items': {'type': 'string'}})
    properties = {key: {'type': 'string'} for key in ('key','shelf','title','raw','summary')}
    properties.update(
        operation={'enum': ['add','update']},
        tags={'type': 'array', 'items': {'type': 'string'}},
        importance={'type': 'number'},
        engram_type={'enum': ['episodic','semantic','procedural']},
        event_ts={'type': ['integer','null']}, actor={'type': ['string','null']},
        location={},
        metadata={'type': 'object', 'additionalProperties': False, 'properties': metadata},
        chapter_id={'type': 'integer'}, expected_revision={'type': 'integer', 'minimum': 1})
    assert set(properties) == RECORD_FIELDS
    record = {'type': 'object', 'additionalProperties': False, 'properties': properties,
              'required': ['key','operation'],
              'oneOf': [{'properties': {'operation': {'const': 'add'}},
                         'required': ['shelf','title','raw']},
                        {'properties': {'operation': {'const': 'update'}},
                         'required': ['chapter_id','expected_revision']}]}
    reference = {'oneOf': [{'type': 'string'},{'type': 'integer'}]}
    link = {'type': 'object', 'additionalProperties': False,
            'properties': {'source': reference, 'target': reference,
                           'link_type': {'type': 'string'}, 'weight': {'type': 'number'},
                           'note': {'type': ['string','null']}},
            'required': ['source','target','link_type']}
    return {'$schema': 'https://json-schema.org/draft/2020-12/schema',
            'title': 'HMK finite capture decision', 'type': 'object',
            'description': 'Structure only; the writer also enforces source, revision, cursor and authority constraints.',
            'additionalProperties': False,
            'properties': {'outcome': {'enum': ['applied','omitted','deferred']},
                           'reason': {'type': 'string','minLength': 1},
                           'selection_version': {'type': 'string','minLength': 1},
                           'records': {'type': 'array','items': record},
                           'links': {'type': 'array','items': link}},
            'required': ['outcome','reason','selection_version']}
