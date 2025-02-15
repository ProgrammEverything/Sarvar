class AttrStopExecutionFlag(Exception):
    """
    Exception raised when execution needs to be stopped due to a _stop flag.
    Used to control program flow and handle critical errors.
    """
    pass
class AttrStopExecution(Exception):
    """
    Exception raised when something in the code has issued an error based on flags or not.
    Used to stop program.
    """
    pass
