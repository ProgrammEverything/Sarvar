from typing import Concatenate, TypeVar, ParamSpec, cast
from functools import wraps
import traceback
from .error_types import AttrStopExecutionFlag, AttrStopExecution
from .Logger import Logger
from .Token import Token
from types import MappingProxyType
from typing import Any, Callable
from typing import Protocol, cast
T = TypeVar("T", bound="Engine")
P = ParamSpec("P")
# Define a Protocol for the decorated function to include attributes
class EngineCommandFunction(Protocol):
    less: int | float
    bigger: int | float
    immutable: bool

    def __call__(self, *args: Any, **kwargs: Any) -> object: ...

def CheckerImplement(func: Callable[Concatenate[T,P], Any]) -> Callable[Concatenate[T,P], Any]:
    """
    In-built decorator for Engine class. Checks If current function or attribute is marked as '_stop'.
    
    Returns:
        Callable: Function with necessary checks added.
    Raises:
        If current function is marked as stop Do not execute function and raise an error with the Function's current arguments shown.
    """
    @wraps(func)
    def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> Any:
        if self._interpret_flags.get(f"{func.__name__}_stop", False):
            raise AttrStopExecutionFlag(f"non-static attribute '{func.__name__}' is marked as '_stop'. arguments: {args}")
        return func(self, *args, **kwargs)
    return  wrapper

def ExecuteIfEnabled(val: str) -> Callable[[Callable[Concatenate[T,P], Any]], Callable[Concatenate[T,P], Any]]:
    """
    Decorator factory for Engine class. Executes the function If a certian specified flag is enabled.
    Args:
        val (str): Value-Key to check.
    Returns:
        Callable: (the wrapper returned) The same function given with flag checks added.
    """
    def decorator(func: Callable[Concatenate[T,P], Any]) -> Callable[Concatenate[T,P], Any]:
        @wraps(func)
        def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> Any:
            if self._interpret_flags[val]:
                return func(self, *args, **kwargs)
        return wrapper
    return decorator

def DebugFunctionIfEnabled(func: Callable[Concatenate[T, P], Any]) -> Callable[Concatenate[T,P], Any]:
    """
    Decorator factory for Engine class. Prints the function's debug through the in-built class debug function If a certian specified flag is enabled.
    Args:
        val (str): Value-Key to check.
    Returns:
        Callable: (the wrapper returned) The same function given with flag checks added.
    """
    @wraps(func)
    def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> Any:
        if self._interpret_flags["PRN_ShowEvents"]:
            self._debug_attr(f"Function '{func.__name__}' is at the start of being executed. Instance: '{self}'. Arguments and Kwargs: '{args}', '{kwargs}'")
            result = func(self, *args, **kwargs)
            self._debug_attr(f"Result of Function '{func.__name__}'s execution . Instance: '{self}'. Arguments and Kwargs: '{args}', '{kwargs}'. Result: '{result}'")
            return result
        return func(self, *args, **kwargs)
    return wrapper

class Engine:
    """
    Engine class for programming and shortcuts.
    Made for easy use for programs and many others.
    Engine class is the main class for interpeting tokens - executing commands and functions.
    Make your first command:
        # First import all of the Engine package
        from Sarvar import *
        # Then make a class instance.
        engine = Engine({}) # Instead of adding commands you could define them like this structure: {"CommandName": Function} as the cmd keyword argument for the Engine class __init__ method.
        # Then add commands using the Engine.engine_command decorator. See docs on Engine.engine_command decorator for more info.
        @Engine.engine_command(bigger_than=0, lesser_than=float("inf"))
        def printContent(token: Token) : # Each function recieves a token. See the Token module docs for more info.
            token.args.append("Print")
            token.args.append(" ".join(token.privatevars))
        # Then add a command
        engine.add_cmd("PRNT", printContent)
        # Then setup a while loop to capture and execute a command based on the built-in input function from python
        while True:
            engine.push_to_stack(input(">>> ")) # Push the input data to command execution stack
            engine.interpret() # Execute current command which is pushed to the stack
        For more info visit: https://github.com/ProgrammEverything/Sarvar
    """
    @staticmethod
    def engine_command(lesser_than: int | float = float("inf"), bigger_than: int | float = float("inf"), macro_immutable: bool=False) -> Callable[[Callable[[Token], None]], EngineCommandFunction]:
        """
        A Decorator factory for registering new engine commands.
        Args:
            command_name (str): Name of the command to register
            lesser_than (int): Maximum number of arguments allowed
            bigger_than (int): Minimum number of arguments required
            macro_immutable (bool): Whether macro expansion should be skipped
            
        Returns:
            Callable: (the wrapper returned) The same function given with attributes defined (All attributes are from the decorator arguments)
        """
        def decorator(func: Callable[[Token], None]) -> EngineCommandFunction:
            @wraps(func)
            def wrapper(token: Token):
                return func(token)
            setattr(wrapper, 'less', lesser_than)
            setattr(wrapper, 'bigger', bigger_than)
            setattr(wrapper, "immutable", macro_immutable)
            return cast(EngineCommandFunction, wrapper)
        return decorator
    @CheckerImplement
    @ExecuteIfEnabled("SHW_OUTPUT")
    def _debug_attr(self: 'Engine', dbg_msg: str) -> None:
        """
        Logs a debug message through the logger.
        
        Args:
            dbg_msg: Message to be logged as debug
        """
        self.currentLogging.log_debug(dbg_msg)
    @CheckerImplement
    @ExecuteIfEnabled("SHW_OUTPUT")
    def _error_attr(self: 'Engine', err_msg: str) -> None:
        """
        Logs an error message through the logger.

        Args:
            err_msg: Error message to be logged
        """
        self.currentLogging.log_error(err_msg)
    @CheckerImplement
    @ExecuteIfEnabled("SHW_OUTPUT")
    def _print_attr(self: 'Engine', prnt_msg: str) -> None:
        """
        Logs a message through the logger.
        
        Args:
            prnt_msg: Message to be printed
        """
        self.currentLogging.log_print(prnt_msg)
    @CheckerImplement
    @ExecuteIfEnabled("SHW_OUTPUT")
    def _warn_attr(self: 'Engine', wrn_msg: str) -> None:
        """
        Logs a warning message through the logger.
        
        Args:
            wrn_msg: Warning message to be logged
        """
        self.currentLogging.log_warning(wrn_msg)
    @CheckerImplement
    @DebugFunctionIfEnabled
    def _make_call_attr(self: 'Engine', call_msg: str) -> None:
        """
        Executes Python code in the public namespace.
        
        Args:
            call_msg (str): Python code to execute
        """
        try:
            exec(call_msg, globals(), {**locals(), **self.Dpublic})
        except Exception:
            self._error_attr(f"Error while executing code {call_msg}. Error:\n{traceback.format_exc()}")
    def __init__(self, cmd: dict[str, EngineCommandFunction], logger: Logger = Logger()):
        # All commands
        # {"Command_name": Function}
        # Function has to be defined by the Engine.engine_command decorator factory
        self.cmd: dict[str, EngineCommandFunction] = cmd
        # Get current logging
        self.currentLogging = logger
        # Public section of all of the variables
        self.Dpublic: dict[str,str]  = dict()
        # All macros
        self.macros: dict[str,str] = {}
        # Current line
        self.current_line = 0
        # Number of all of the lines. Needs to be updated If a new command is inserted
        self.all_lines = 0
        # List of the execution stack
        self.commands: list[str] = []
        # Interpreter flags for better control
        self._interpret_flags = {
            "PRN_ShowEvents": False,
            "BOL_HNDLE_DBGLST": True,
            "SHW_OUTPUT": True,
            "INTERP_EXEC_EVEN_IF_ERROR": False,
            "INTERP_EXEC_EVEN_IF_RAISED": False
        }
        # ReadView for the Flags property
        self.readView = MappingProxyType(self._interpret_flags)
        # Commands for the Token to use
        self.defaultVars: dict[str, Callable[..., object]] = {
            "Warn": self._warn_attr,
            "Error": self._error_attr,
            "Debug": self._debug_attr,
            "Print": self._print_attr,
            "MakeCall": self._make_call_attr,
        }
    @CheckerImplement
    @ExecuteIfEnabled("BOL_HNDLE_DBGLST")
    @DebugFunctionIfEnabled
    # Handles Token.args
    def _handle_debug_list(self, dbg_list: list[str]):
        
        if len(dbg_list) <= 1:
            return
        index = 0
        ln_dbglst = len(dbg_list)
        while index < ln_dbglst:
            citem = dbg_list[index]
            if index + 1 > ln_dbglst-1:
                break
            nitem = dbg_list[index+1]
            if citem in self.defaultVars:
                self.defaultVars[citem](nitem)
                index += 1
            elif citem.startswith("_" , 0, 1) and citem.replace(" ", ""):
                self.push_to_stack(citem[1:] + " " + nitem)
                self.current_line+=1
                self.interpret()
                index+=1
            index += 1
    @DebugFunctionIfEnabled
    def add_cmd(self, cmd: str, func: EngineCommandFunction):
        """
        Registers a new command in the engine.
        
        Args:
            cmd (str): Command name
            func (EngineCommandFunction): Function to execute for this command. Has to support "EngineCommandFunction" protocol. (Defined by the Engine.engine_command decorator factory)
        """
        self.cmd[cmd] = func
    @DebugFunctionIfEnabled
    def remove_cmd(self, cmd: str):
        """
        Removes a command from the engine.
        
        Args:
            cmd (str): Command name to remove
        """
        del self.cmd[cmd]
        """
        Function made to handle all programming requests - handling stack - cleaning and etc...
        """
    @DebugFunctionIfEnabled
    def push_to_stack(self, commandLineArguments: str):
        """
        Adds a new command to the execution stack.
        
        Args:
            commandLineArguments: Command arguments to be added
        """
        self.commands.append(commandLineArguments)
        self.all_lines += 1
    @DebugFunctionIfEnabled
    def interpret(self):
        """
        Interprets and executes the current command line.

        Raises:
            Various exceptions based on command execution and flags
        """
        # Check If it's on the current line
        if self.current_line >= self.all_lines and not self._interpret_flags["INTERP_EXEC_EVEN_IF_ERROR"]:
            raise AttrStopExecution(f"Current line '{self.current_line}' is bigger or equal to 'all_lines' value: '{self.all_lines}'")
        # Find current command
        cli_args = self.commands[self.current_line]
        # Split the command line arguments
        cli_args_split = self.commands[self.current_line].split()
        # If there are no arguments, skip
        # If argument = 0 : not 0 -> 1 So the program adds one to current_line and then returns
        if not len(cli_args_split): self.current_line+=1; return
        # Get the command name
        command_name = cli_args_split[0]
        # Check If the command exists
        if command_name in self.cmd:
            # Check If the command is not immutable
            if not self.cmd[command_name].immutable:
                # If not, expand the macros
                for item,key in self.macros.items():
                    cli_args = cli_args.replace(item, key)
            # Split the command line arguments
            cli_args = cli_args.split()
            # Check If the number of arguments is correct
            if not len(cli_args[1:]) < self.cmd[command_name].less:
                self._error_attr(f"Command line arguments must be lesser than {self.cmd[command_name].less}.\nLIMIT: {self.cmd[command_name].less}.\nNUMBER OF ARGUMENTS: {len(cli_args[1:])}.")
                if not self._interpret_flags["INTERP_EXEC_EVEN_IF_ERROR"]:
                    self.current_line+=1 
                    return
            # Check If the number of arguments is correct
            elif not len(cli_args[1:]) > self.cmd[command_name].bigger:
                self._error_attr(f"Command line arguments must be bigger than {self.cmd[command_name].bigger}.\nLIMIT: {self.cmd[command_name].bigger}.\nNUMBER OF ARGUMENTS: {len(cli_args[1:])}.")
                if not self._interpret_flags["INTERP_EXEC_EVEN_IF_ERROR"]: 
                    self.current_line+=1
                    return
            # Create a Token for command function
            current_token = Token(globalvars=self.Dpublic, privatevars=cli_args[1:], macros=self.macros, current_line=self.current_line, all_lines=self.all_lines)
            try:
                # If command execution fails, raise an error or log into Logger based on the flag else do not raise or log anything
                self.cmd[command_name](current_token)
            except Exception as error:
                query = f"Error while executing command on line '{self.current_line}' Command: '{command_name}'."
                if not self._interpret_flags["INTERP_EXEC_EVEN_IF_RAISED"]:
                    raise AttrStopExecution(query) from error
                else:
                    self._error_attr(query + "Error: " + str(traceback.format_exc()))
            # Handle debug list
            # Note that If the command execution actually logs anything into Token.args and then has an execution error. The parts pushed into the debug_list will be still showed and the command will be raised or not based on the flag.
            self._handle_debug_list(current_token.args)
            # Update the public namespace
            self.Dpublic = current_token.globalvars
            # Update the current line If it changes
            if current_token.current_line != self.current_line:
                self.current_line = current_token.current_line
            else:
                # Else add 1
                self.current_line+=1
            # If the flag is enabled, log the execution
            if self._interpret_flags["PRN_ShowEvents"]:
                self._debug_attr(f"Current line:\t'{self.current_line}'\tAll lines: '{self.all_lines}'\ttoken: '{current_token}'\tcommand: '{command_name}'\tCommand-line-arguments:  {cli_args}")
        else:
            # If command not found log an error
            self._error_attr(f"Cannot find command {command_name} not found.")
            # Add 1 to current_line
            self.current_line += 1
        
    @DebugFunctionIfEnabled
    def HELPER_InterepetAll(self):
        """
        Executes all commands in the stack until completion.
        Continues execution until current_line reaches all_lines.
        """
        while self.current_line < self.all_lines:
            self.interpret()
    @property
    @DebugFunctionIfEnabled
    def get_cmd(self):
        """
        Property that returns the command dictionary.
        
        Returns:
            dict: Dictionary of registered commands
        """
        return self.cmd
    @property
    @DebugFunctionIfEnabled
    def Flags(self):
        """
        ReadView of the self._interpret_flags
        Returns:
            MappingProxyType: self.readView view of the flags
        """
        return self.readView
    @DebugFunctionIfEnabled
    def set_flag(self, name: str, val: bool) -> None:
        """
        Sets a flag in the interpreter
        Args:
            name (str): Flag name to set 
            val (bool): Value to set
        """
        # Sets flag
        self._interpret_flags[name] = val
    @DebugFunctionIfEnabled
    def unset_flag(self, arg: str):
        # Unset flag - !self._interpret_flags[arg]
        self._interpret_flags[arg] = not self._interpret_flags[arg]