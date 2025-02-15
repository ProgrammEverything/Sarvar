import rich
from sys import stdout, stderr
from typing import TextIO
class Logger:
    """
    Handles different types of logging output with color formatting.
    
    Attributes:
        error_file: File descriptor for error output
        input_file: File descriptor for input
        debug_file: File descriptor for debug messages
        print_file: File descriptor for standard output
        warn_file: File descriptor for warnings
    """
    def __init__(self, def_debug: TextIO = stdout, def_warn: TextIO = stderr, def_print: TextIO = stdout, def_err: TextIO = stderr):
        self.error_file = def_err
        self.debug_file = def_debug
        self.print_file = def_print
        self.warn_file  = def_warn
    def log_error(self, it: str): rich.print("[red]"+ "ERROR:\t" +str(it)+"[/red]", file=self.error_file)
    def log_warning(self, it: str): rich.print("[yellow]" + "WARNING:\t" +str(it)+"[/yellow]", file=self.warn_file)
    def log_debug(self, it: str): rich.print("[blue]"+ "DEBUG:\t" + str(it)+"[/blue]", file=self.debug_file)
    def log_print(self, it: str): rich.print("[cyan]OUTPUT:\t"+str(it)+"[/cyan]", file =self.print_file)

