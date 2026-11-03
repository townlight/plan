"""Released source-provider contract. Callables are injected by trusted runtime code."""
import hashlib


class ConnectionUnavailable(RuntimeError):
    pass


def permitted(providers, link):
    provider = providers.get(link['provider'])
    if not callable(provider):
        raise ConnectionUnavailable('Connected source provider unavailable; saved work is retained.')
    try:
        rows = provider(source_id=link['source_id'])
    except Exception:
        raise ConnectionUnavailable('Connected source unavailable; no cached source substituted.') from None
    if not isinstance(rows, (list, tuple)) or len(rows) != 1:
        raise ConnectionUnavailable('Connected source no longer resolves exactly once.')
    doc = rows[0]
    if not isinstance(doc, dict) or doc.get('visibility') != 'public' or not isinstance(doc.get('text'), str):
        raise ConnectionUnavailable('Connected source is not permitted.')
    digest = hashlib.sha256(doc['text'].encode()).hexdigest()
    if doc.get('source_id') != link['source_id'] or digest != link['expected_sha256'] or doc.get('sha256') != digest:
        raise ConnectionUnavailable('Connected source changed; staff must select its current version.')
    return {k: doc[k] for k in ('source_id', 'title', 'text', 'sha256', 'visibility', 'version', 'citation')}


def search(providers, provider_name, query):
    provider = providers.get(provider_name)
    if not callable(provider):
        raise ConnectionUnavailable('Connected source provider unavailable.')
    try:
        rows = provider(query=query)
    except Exception:
        raise ConnectionUnavailable('Connected source search unavailable; no cached results.') from None
    if not isinstance(rows, (list, tuple)):
        raise ConnectionUnavailable('Connected source provider returned invalid results.')
    result = []
    for row in rows[:50]:
        if not isinstance(row, dict) or row.get('visibility') != 'public':
            continue
        doc = permitted(providers, {'provider': provider_name, 'source_id': row.get('source_id'),
                                   'expected_sha256': row.get('sha256')})
        result.append({k: v for k, v in doc.items() if k != 'text'} | {'excerpt': doc['text'][:500]})
    return {'results': result, 'truncated': len(rows) > 50}
