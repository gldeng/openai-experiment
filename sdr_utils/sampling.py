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
