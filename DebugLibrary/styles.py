from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style

NORMAL_STYLE = Style.from_dict({
    'head': 'fg:green',
    'message': 'fg:silver',
})

ERROR_STYLE = Style.from_dict({
    'head': 'fg:red',
    'message': 'fg:white',
})

DEBUG_PROMPT_STYLE = Style.from_dict({
    'prompt': 'blue',
})


def print_output(head, message, style=NORMAL_STYLE):
    """Print prompt-toolkit tokens to output."""
    tokens = FormattedText([
        ('class:head', '{0} '.format(head)),
        ('class:message', message),
        ('', ''),
    ])
    print_formatted_text(tokens, style=style)


def print_error(head, message, style=ERROR_STYLE):
    """Print to output with error style."""
    print_output(head, message, style=style)


def get_debug_prompt_tokens(prompt_text):
    """Print prompt-toolkit prompt."""
    return [
        ('class:prompt', prompt_text),
    ]
