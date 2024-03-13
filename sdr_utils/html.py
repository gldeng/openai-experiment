
from .constants import DALLE_RESULT_FIELD_NAME, LEONARDO_RESULT_FIELD_NAME

pipeline = [
    # {'$match': {'$or': [{DALLE_RESULT_FIELD_NAME: {'$ne': None}}, {LEONARDO_RESULT_FIELD_NAME: {'$ne': None}}]}},
    {
        '$project': {
            '_id': 0,
            'prompt': 1,
            'revised_prompt': { '$arrayElemAt': [f'${DALLE_RESULT_FIELD_NAME}.data.revised_prompt', 0] },
            'original_prompt': 1,
            'trait_args': 1,
            'image': 1,
            'image256': 1
        }
    }
]

_keys = [
    'image256',
    'prompt',
    'revised_prompt',
    'original_prompt',
    'traits'
]


def get_docs(coll):
    docs = list(sorted(coll.aggregate(pipeline), key=lambda x: len(x['prompt'])))
    for doc in docs:
        doc['traits'] = str(len(doc['trait_args'])) + ' traits' + ':\n' + '\n'.join(
            ['[{}]: {}'.format(trait['traitType'], trait['value']) for trait in doc['trait_args']]
        )
    return docs


def _prepare_th(doc, key):
    if key in ['image', 'image256']:
        return f"<td><img src='data:image/png;base64,{doc.get(key, '')}' width='200px'></td>"
    
    value = doc.get(key, '')
    value = '' if not value else value.replace('\n', '<br/>')
    return f'<td>{value}</td>'

def _prepare_header():

    ths = [f'<th>{key}</th>' for key in _keys]
    header = f'<tr>{"".join(ths)}</tr>'
    return header


def prepare_table(docs):
    header = _prepare_header()
    rows = []
    # Loop through each JSON object to add a row in the table
    for doc in docs:
        tds = [_prepare_th(doc, key) for key in _keys]
        row = f'<tr>{"".join(tds)}</tr>'
        rows.append(row)
    body = '\n'.join(rows)
    table = f'<table>{header}\n{body}</table>'
    return table


def write_html(filename, html):
    with open(filename, "w") as file:
        file.write(html)
