import cmd
import os

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle, prompt


class BaseCmd(cmd.Cmd):
    """Basic REPL tool."""
    prompt = '> '
    repeat_last_nonempty_command = False

    def emptyline(self):
        """Do not repeat the last command if input empty unless forced to."""
        if self.repeat_last_nonempty_command:
            return super(BaseCmd, self).emptyline()
        return None

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

    def pre_loop_iter(self):
        """Excute before every loop iteration."""

    def _get_input(self):
        if self.cmdqueue:
            return self.cmdqueue.pop(0)
        else:
            try:
                return self.get_input()
            except KeyboardInterrupt:
                return None

    def loop_once(self):
        self.pre_loop_iter()
        line = self._get_input()
        if line is None:
            return None

        if line == 'exit':
            line = 'EOF'

        line = self.precmd(line)
        if line == 'EOF':
            # do not run 'EOF' command to avoid override 'lastcmd'
            stop = True
        else:
            stop = self.onecmd(line)
        stop = self.postcmd(stop, line)
        return stop

    def cmdloop(self, intro=None):
        """Better command loop.

        override default cmdloop method
        """
        if intro is not None:
            self.intro = intro
        if self.intro:
            self.stdout.write(self.intro)
            self.stdout.write('\n')

        self.preloop()

        stop = None
        while not stop:
            stop = self.loop_once()

        self.postloop()

    def get_input(self):
        return input(prompt=self.prompt)


class PromptToolkitCmd(BaseCmd):
    """CMD shell using prompt-toolkit."""

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

    def get_input(self):
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
        except EOFError:
            line = 'EOF'
        return line
