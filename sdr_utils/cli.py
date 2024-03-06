import click
from .html import get_docs, prepare_table, write_html
from .sampling import generate_progressive_samples, generate_samples
from .mongo import get_collection, create_collection_if_not_exists
from .prompt import ensure_as_is, generate_prompt
from .generation import run_one_sample, run_one_leonardo_sample
from .constants import BASE_PROMPT
from .reorg import run_reorg


@click.group()
def cli():
    pass

@click.command()
@click.option('--db-name', default="", help='MongoDB name used for this run. If supplied, the sample will be stored in the MongoDB.')
@click.option('--base-prompt', default=BASE_PROMPT, help='The base prompt.')
@click.argument('filename')
def sample(filename, db_name, base_prompt):
    def _make_prompt(base_prompt, trait_args):
        prompt = generate_prompt(base_prompt, trait_args)
        prompt = run_reorg(prompt)
        prompt = ensure_as_is(prompt)
        return prompt

    import json
    with open(filename, 'r') as fi:
        trait_definitions = json.load(fi)
    samples = generate_samples(trait_definitions)
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
@click.option('-u', '--use-leonardo', default="False", help='Use Leonardo API to generate images.')
@click.option('-a', '--leonardo-api-key', default="", help='The API key for Leonardo.')
@click.option('-i', '--image-file-path', default="", help='The path to the image file to be used as input for Leonardo.')
def generate(db_name, use_leonardo=False, leonardo_api_key="", image_file_path=""):
    coll = get_collection(db_name)
    sample_items = list(coll.find({}))

    if use_leonardo == True:
        prev_doc = ""
        for sample_item in sample_items:
            print(sample_item['prompt'])
            doc = coll.find_one({'prompt': sample_item['prompt']}, {'_id': 0})
            res = run_one_leonardo_sample(doc, sample_item, image_file_path, leonardo_api_key)
            coll.update_one({'prompt': doc['prompt']}, {'$set': res})
            prev_doc = doc
    else:
        for sample_item in sample_items:
            print(sample_item['prompt'])
            res = run_one_sample(coll, sample_item)


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



cli.add_command(sample)
cli.add_command(sample_progressive)
cli.add_command(generate)
cli.add_command(html)


def main():
    cli()
