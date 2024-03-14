import click
import os
from .html import get_docs, prepare_table, write_html
from .sampling import generate_progressive_samples, generate_samples
from .mongo import get_collection, create_collection_if_not_exists
from .prompt import ensure_as_is, generate_prompt
from .generation import run_one_sample, run_one_leonardo_sample
from .constants import BASE_PROMPT, LEONARDO_API_KEY_NAME
from .reorg import reorg_prompt, run_reorg
from .sample_new_traits import Sampler
from .quality_check import detect_bad


@click.group()
def cli():
    pass

@click.command()
@click.option('-d', '--db-name', default="", help='MongoDB name used for this run. If supplied, the sample will be stored in the MongoDB.')
@click.option('-p', '--base-prompt', default=BASE_PROMPT, help='The base prompt.')
@click.option('-n', '--sample-size', default=100, help='The number of samples to create. Default to 100.')
@click.option('-r', '--reorg', default=False, help='With reorg.')
@click.argument('traits_dir')
def sample(traits_dir, db_name, base_prompt, sample_size, reorg):
    def _prepare_doc(trait_args):
        p = generate_prompt(base_prompt, trait_args)
        if not reorg:
            return {'prompt': p, 'trait_args': trait_args}
        prefix = ''
        prompt = p
        if ':' in p:
            prefix, prompt = p.split(':')
        if reorg:
            new_prompt = run_reorg(prompt)
            if prefix:
                new_prompt = ': '.join([prefix, new_prompt])
        return {'prompt': new_prompt, 'original_prompt': p, 'trait_args': trait_args}

    coll = None
    if db_name != "":
        create_collection_if_not_exists(db_name)
        coll = get_collection(db_name)
    sampler = Sampler(traits_dir)
    samples = sampler.sample(sample_size)
    for s in samples:
        doc = _prepare_doc(s)
        if coll != "":
            coll.insert_one(doc)
        else:
            print(doc['prompt'])


@click.command()
@click.option('-d', '--db-name', default="", help='MongoDB name used for this run. If supplied, the sample will be stored in the MongoDB.')
@click.option('-p', '--base-prompt', default=BASE_PROMPT, help='The base prompt.')
@click.option('-e', '--extra-desc', default="", help='Extra description about the image.')
@click.option('-n', '--num-last-gen', default=1, help='The number of samples in the last generations. The ancestors will be derived from them.')
@click.option('-R', '--no-reorg', default=False, help='Disable reorganization of sentences by GPT-4.')
@click.argument('filename')
def sample_progressive(filename, db_name, base_prompt, extra_desc, num_last_gen, no_reorg):
    def _maybe_append_extra(prompt):
        return f"{prompt} {extra_desc.strip()}" if extra_desc.strip() else prompt

    def _make_prompt(base_prompt, trait_args):
        prompt = generate_prompt(base_prompt, trait_args)
        prompt = _maybe_append_extra(prompt)
        if not no_reorg:
            prompt = run_reorg(prompt)
        prompt = ensure_as_is(prompt)
        return prompt

    
    import json
    with open(filename, 'r') as fi:
        trait_definitions = json.load(fi)
    samples = generate_progressive_samples(trait_definitions, num_last_gen)
    sample_with_prompts = list(map(lambda x: {'prompt': _make_prompt(base_prompt, x), 'trait_args': x}, samples))
    if db_name != "":
        create_collection_if_not_exists(db_name)
        coll = get_collection(db_name)
        coll.insert_many(sample_with_prompts)
        print(f"Samples are stored in db {db_name}")
    else:
        print('\n'.join([s['prompt'] for s in sample_with_prompts]))


@click.command()
@click.option('-d', '--db-name', default="", help='MongoDB name used for this run. If supplied, the sample will be stored in the MongoDB.')
@click.argument('base_image_filename')
def leonardo(base_image_filename, db_name):
    coll = get_collection(db_name)
    sample_items = list(coll.find({}))
    leonardo_api_key = os.environ[LEONARDO_API_KEY_NAME]

    parent_doc = None
    for sample_item in sample_items:
        print(sample_item['prompt'])
        doc = coll.find_one({'prompt': sample_item['prompt']}, {'_id': 0})
        res = run_one_leonardo_sample(parent_doc, doc, sample_item, base_image_filename, leonardo_api_key)
        coll.update_one({'prompt': doc['prompt']}, {'$set': res})
        doc.update(res)
        parent_doc = doc


@click.command()
@click.option('-d', '--db-name', default="", help='MongoDB name used for this run. If supplied, the sample will be stored in the MongoDB.')
def generate(db_name):
    coll = get_collection(db_name)
    sample_items = list(coll.find({}))
    for sample_item in sample_items:
        print(sample_item['prompt'])
        res = run_one_sample(coll, sample_item)


@click.command()
@click.option('-d', '--db-name', default="", help='MongoDB name used for this run. If supplied, the sample will be stored in the MongoDB.')
def check(db_name):
    coll = get_collection(db_name)
    sample_items = list(coll.find({'image256': {'$ne': None}}))
    for sample_item in sample_items:
        print(sample_item['prompt'])
        res = detect_bad(sample_item['image256'])
        quality_bad = 'true' in res['choices'][0]['message']['content']
        coll.update_one(
            {'prompt': sample_item['prompt']},
            {'$set':{'quality_check': res, 'quality_bad': quality_bad}}
        )


@click.command()
@click.option('-d', '--db-name', help='MongoDB name used for this run. If supplied, the sample will be stored in the MongoDB.')
@click.option('-o', '--output', default="", help='The output file name (if not supplied, db-name will be used).')
def html(db_name, output):
    coll = get_collection(db_name)
    docs = get_docs(coll)
    table = prepare_table(docs)
    if output == "":
        output = db_name+'.html'
    write_html(output, table)


@click.command()
@click.option('-d', '--db-name', default="", help='MongoDB name used for this run. If supplied, the sample will be stored in the MongoDB.')
def reorg(db_name):
    coll = get_collection(db_name)
    sample_items = list(coll.find({'reorg': {'$eq': None}}))
    for sample_item in sample_items:
        print(sample_item['prompt'])
        res = reorg_prompt(coll, sample_item)


cli.add_command(sample)
cli.add_command(sample_progressive)
cli.add_command(generate)
cli.add_command(leonardo)
cli.add_command(check)
cli.add_command(html)


cli.add_command(reorg)


def main():
    cli()
