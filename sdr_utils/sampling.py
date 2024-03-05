from random import sample

from dataclasses import dataclass, field
from typing import List

@dataclass
class TraitDefinition:
    name: str
    values: List[str]

@dataclass
class TraitDefinitions:
    defintions: List[TraitDefinition] = field(default_factory=list)


def sample_trait_values(trait_definitions: TraitDefinitions, num):
    traits = []
    for trait in sample(trait_definitions, num):
        traits.append({'name': trait['name'], 'value': sample(trait['values'], 1)[0]})
    return traits


def generate_samples(trait_definitions: TraitDefinitions):
    samples = []
    for num in range(1, len(trait_definitions)+1):
        for _ in range(10):
            samples.append(sample_trait_values(trait_definitions, num))
    return samples


def _parent_gen(traits):
    return sample(traits, len(traits)-1)


def generate_progressive_samples(trait_definitions: TraitDefinitions, num_of_last_gen_samples=2):
    samples = []
    num = len(trait_definitions) # sample last generation
    last_gen_samples = []
    for _ in range(num_of_last_gen_samples):
        last_gen_samples.append(sample_trait_values(trait_definitions, num))
    samples.extend(last_gen_samples)
    cur_samples = last_gen_samples
    while len(cur_samples[0]) > 1:
        # need to check parent
        cur_samples = [_parent_gen(sample) for sample in cur_samples]
        samples.extend(cur_samples)
    return list(reversed(samples))
