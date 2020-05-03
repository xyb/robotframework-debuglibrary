import cmd
import os

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle, prompt


class BaseCmd(cmd.Cmd):
    """Basic REPL tool."""

    def emptyline(self):
        """Do not repeat last command if press enter only."""

    def do_exit(self, arg):
        """Exit the interpreter. You can also use the Ctrl-D shortcut."""

        return True

    do_EOF = do_exit

    def help_help(self):
        """Help of Help command"""

        print('Show help message.')

    def do_pdb(self, arg):
        """Enter the python debuger pdb. For development only."""
        print('break into python debugger: pdb')
        import pdb
        pdb.set_trace()

    def get_cmd_names(self):
        """Get all command names of CMD shell."""
        pre = 'do_'
        cut = len(pre)
        return [_[cut:] for _ in self.get_names() if _.startswith(pre)]

    def get_help_string(self, command_name):
        """Get help document of command."""
        func = getattr(self, 'do_{0}'.format(command_name), None)
        if not func:
            return ''
        return func.__doc__

    def get_helps(self):
        """Get all help documents of commands."""
        return [(name, self.get_help_string(name) or name)
                for name in self.get_cmd_names()]

    def get_completer(self):
        """Get completer instance."""

    def pre_loop(self):
        """Excute before every loop iteration."""


class PromptToolkitCmd(BaseCmd):
    """CMD shell using prompt-toolkit."""

    prompt = '> '
    get_prompt_tokens = None
    prompt_style = None
    intro = '''\
Only accepted plain text format keyword separated with two or more spaces.
Type "help" for more information.\
'''

    def __init__(self, completekey='tab', stdin=None, stdout=None,
                 history_path=''):
        BaseCmd.__init__(self, completekey, stdin, stdout)
        self.history = FileHistory(os.path.expanduser(history_path))

    def cmdloop(self, intro=None):
        """Better command loop supported by prompt_toolkit.

        override default cmdloop method
        """
        if intro is not None:
            self.intro = intro
        if self.intro:
            self.stdout.write(self.intro)
            self.stdout.write('\n')

        stop = None
        while not stop:
            self.pre_loop()
            if self.cmdqueue:
                line = self.cmdqueue.pop(0)
            else:
                kwargs = dict(
                    history=self.history,
                    auto_suggest=AutoSuggestFromHistory(),
                    enable_history_search=True,
                    completer=self.get_completer(),
                    complete_style=CompleteStyle.MULTI_COLUMN,
                )
                if self.get_prompt_tokens:
                    kwargs['style'] = self.prompt_style
                    prompt_str = self.get_prompt_tokens(self.prompt)
                else:
                    prompt_str = self.prompt
                try:
                    line = prompt(message=prompt_str, **kwargs)
                except KeyboardInterrupt:
                    continue
                except EOFError:
                    line = 'EOF'

            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)

        self.postloop()
