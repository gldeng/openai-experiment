
from .constants import DALLE_RESULT_FIELD_NAME, LEONARDO_RESULT_FIELD_NAME

pipeline = [
    {'$match': {'$or': [{DALLE_RESULT_FIELD_NAME: {'$ne': None}}, {LEONARDO_RESULT_FIELD_NAME: {'$ne': None}}]}},
    {
        '$project': {
            '_id': 0,
            'prompt': 1,
            'revised_prompt': { '$arrayElemAt': [f'${DALLE_RESULT_FIELD_NAME}.data.revised_prompt', 0] },
            'image': 1,
            'image256': 1
        }
    }
]

_keys = [
    'image256',
    'prompt',
    'revised_prompt'
]


def get_docs(coll):
    return list(sorted(coll.aggregate(pipeline), key=lambda x: len(x['prompt'])))


def _prepare_th(doc, key):
    if key in ['image', 'image256']:
        return f"<td><img src='data:image/png;base64,{doc[key]}' width='200px'></td>"
    
    return f'<td>{doc[key]}</td>'

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
