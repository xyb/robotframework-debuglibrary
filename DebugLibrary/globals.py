class SingletonContext:
    in_step_mode = False
    current_runner = None
    current_runner_step = None
    current_source_path = ''
    current_source_lineno = 0
    last_command = ''

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonContext, cls).__new__(cls)
        return cls.instance


context = SingletonContext()
