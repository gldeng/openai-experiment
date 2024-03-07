from .constants import AS_IS_PREFIX, BASE_PROMPT
import execjs
from importlib import resources

def _get_default_prompt_script():
    with resources.open_text('sdr_utils.resources', 'createPrompt.js') as f:
        data = f.read()
    return data

_ctx = execjs.compile(_get_default_prompt_script())


def generate_prompt(base_prompt, trait_args):
    cfg = {
        'prefix': base_prompt
    }
    prompt = _ctx.call('createPrompt', cfg, trait_args)
    return prompt


def ensure_as_is(prompt):
    if AS_IS_PREFIX not in prompt:
        return f'{AS_IS_PREFIX} {prompt}'
    else:
        return prompt
