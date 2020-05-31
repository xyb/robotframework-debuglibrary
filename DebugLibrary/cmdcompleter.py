from prompt_toolkit.completion import Completer, Completion

from .robotkeyword import parse_keyword


class CmdCompleter(Completer):
    """Completer for debug shell."""

    def __init__(self, commands, cmd_repl=None):
        self.names = []
        self.displays = {}
        self.display_metas = {}
        for name, display, display_meta in commands:
            self.names.append(name)
            self.displays[name] = display
            self.display_metas[name] = display_meta
        self.cmd_repl = cmd_repl

    def _get_argument_completions(self, completer, document):
        """Using Cmd.py's completer to complete arguments."""
        end_idx = document.cursor_position_col
        line = document.current_line
        if line[:end_idx].rfind(' ') >= 0:
            begin_idx = line[:end_idx].rfind(' ') + 1
        else:
            begin_idx = 0
        prefix = line[begin_idx:end_idx]

        completions = completer(prefix, line, begin_idx, end_idx)
        for comp in completions:
            yield Completion(comp, begin_idx - end_idx, display=comp)

    def _get_custom_completions(self, cmd_name, document):
        completer = getattr(
            self.cmd_repl,
            'complete_{0}'.format(cmd_name),
            None,
        )
        if completer:
            yield from self._get_argument_completions(completer, document)

    def _get_command_completions(self, text):
        return (Completion(name,
                           -len(text),
                           display=self.displays.get(name, ''),
                           display_meta=self.display_metas.get(name, ''),
                           )
                for name in self.names
                if ((('.' not in name and '.' not in text)  # root level
                     or ('.' in name and '.' in text))  # library level
                    and name.lower().strip().startswith(text.strip()))
                )

    def get_completions(self, document, complete_event):
        """Compute suggestions."""
        text = document.text_before_cursor.lower()
        parts = parse_keyword(text)

        if len(parts) >= 2:
            cmd_name = parts[0].strip()
            yield from self._get_custom_completions(cmd_name, document)
        else:
            yield from self._get_command_completions(text)
