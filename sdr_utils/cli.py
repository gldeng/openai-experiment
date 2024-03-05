import click
from .sampling import generate_samples
from .mongo import get_collection, create_collection_if_not_exists
from .prompt import generate_prompt
from .constants import BASE_PROMPT


@click.group()
def cli():
    pass

@click.command()
@click.option('--db-name', default="", help='MongoDB name used for this run. If supplied, the sample will be stored in the MongoDB.')
@click.option('--base-prompt', default=BASE_PROMPT, help='The base prompt.')
@click.argument('filename')
def sample(filename, db_name, base_prompt):
    import json
    with open(filename, 'r') as fi:
        trait_definitions = json.load(fi)
    samples = generate_samples(trait_definitions)
    sample_with_prompts = list(map(lambda x: {'prompt': generate_prompt(base_prompt, x), 'trait_args': x}, samples))
    if db_name != "":
        create_collection_if_not_exists(db_name)
        coll = get_collection(db_name)
        coll.insert_many(sample_with_prompts)
    else:
        print(json.dumps(sample_with_prompts))


@click.command()
@click.argument('filename')
def sample_progressive(filename):
    click.echo(f'Hello {filename}!')


@click.command()
@click.argument('filename')
def sample_progressive(name):
    click.echo(f'Hello {name}!')


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.argument('name')
def repeat_greet(name, count):
    for _ in range(count):
        click.echo(f'Hello {name}!')


cli.add_command(sample)
cli.add_command(sample_progressive)


def main():
    cli()
