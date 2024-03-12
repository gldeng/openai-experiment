import os
import json
import random

class Sampler:
    base3 = ['background', 'breed', 'clothes']

    def __init__(self, traits_dir):
        self.traits_dir = traits_dir
        all_trait_types = [f.split('.')[0] for f in os.listdir(traits_dir)]
        nonbase3 = [tt for tt in all_trait_types if tt not in self.base3]
        self.base3_traits = {
            tt: self._get_trait_values(tt)
            for tt in self.base3
        }
        self.nonbase3_traits = {
            tt: self._get_trait_values(tt)
            for tt in nonbase3
        }

    def _get_trait_values(self, tt):
        with open(os.path.join(self.traits_dir, tt+'.json'), 'r') as fi:
            return json.load(fi)

    def sample(self, n):
        output = []
        for i in range(n):
            trait_args = []
            for (tt, values) in self.base3_traits.items():
                trait_args.append({'traitType': tt, 'value': random.sample(values, 1)[0]})
            additional_count = random.randint(1,6)
            for (tt, values) in random.sample(list(self.nonbase3_traits.items()), additional_count):
                trait_args.append({'traitType': tt, 'value': random.sample(values, 1)[0]})
            output.append(trait_args)
        return output
