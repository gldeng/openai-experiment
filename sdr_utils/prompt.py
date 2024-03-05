from .constants import BASE_PROMPT


def _concat(items):
    if len(items) > 1:
        return ', '.join(items[:-1]) + ' and '+items[-1]
    return ', '.join(items)


def _strip_all(items):
    return list(map(lambda x: x.strip(), items))


def generate_prompt(base_prompt, trait_args):
    prompt = base_prompt.strip()
    category_is = []
    category_with = []
    category_pet = []
    for t in trait_args:
        value = t['value'].lower()
        if 'is' in value and 'is wearing' not in value:
            category_is.append(value.replace('is ', ' '))
        elif t['name'].lower() == 'pet':
            category_pet.append('pet ' + value)
        else:
            category_with.append(value.replace('wearing', '').replace('is wearing', '').replace('has', ''))
    only_is = category_is and not category_with
    both = category_is and category_with
    only_with = not category_is and category_with
    desc_is = 'that is ' + _concat(_strip_all(category_is))
    desc_with = 'with ' + _concat(_strip_all(category_with))
    if only_is:
        prompt += ' ' + desc_is.strip()
    if only_with:
        prompt += ' ' + desc_with.strip()
    if both:
        prompt += f' {desc_is.strip()} and {desc_with.strip()}'
    if category_pet:
        prompt += '. It is accompanied by a ' + ', '.join(category_pet)
    prompt += '.'
    return prompt