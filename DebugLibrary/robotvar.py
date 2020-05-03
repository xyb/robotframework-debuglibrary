def assign_variable(robot_instance, variable_name, args):
    """Assign a robotframework variable."""
    variable_value = robot_instance.run_keyword(*args)
    robot_instance._variables.__setitem__(variable_name, variable_value)
    return variable_value
