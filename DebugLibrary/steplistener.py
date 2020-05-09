import inspect

from .globals import context


class RobotLibraryStepListenerMixin:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        super(RobotLibraryStepListenerMixin, self).__init__()
        self.ROBOT_LIBRARY_LISTENER = [self]

    def _start_keyword(self, name, attrs):
        context.current_source_path = ''
        context.current_source_lineno = 0

        if not is_step_mode():
            return

        find_runner_step()
        step = context.current_runner_step

        if hasattr(step, 'lineno'):
            path = step.source
            lineno = step.lineno
            lineno_0_based = lineno - 1
            context.current_source_path = path
            context.current_source_lineno = lineno
            print('> {}({})'.format(path, lineno))
            line = (open(path).readlines()[lineno_0_based].strip())
            print('-> {}'.format(line))

        if attrs['assign']:
            assign = '%s = ' % ', '.join(attrs['assign'])
        else:
            assign = ''
            name = '{}.{}'.format(attrs['libname'], attrs['kwname'])

        translated = '{}{}  {}'.format(assign, name, '  '.join(attrs['args']))
        print('=> {}'.format(translated))

        # callback debug interface
        self.debug()


def find_runner_step():
    stack = inspect.stack()
    for frame in stack:
        if frame.function == 'run_steps':
            arginfo = inspect.getargvalues(frame.frame)
            context.current_runner = arginfo.locals.get('runner')
            context.current_runner_step = arginfo.locals.get('step')


def set_step_mode(on=True):
    context.in_step_mode = on


def is_step_mode():
    return context.in_step_mode
