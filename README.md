# Sarvar
A simple assembly like interpreter implementation. 
Good for programs which need command shortcuts or command lines for their programs.\
Not good in speed but good in simplicity.
## Installation
(REQUIRES PYTHON>=3.8)\
How to install on windows:\
    ```
    py -m pip install Sarvar
    ```\
How to install on mac, linux, ... : (PIP HAS TO BE INSTALLED)\
    -```
    python3 -m pip install Sarvar
    ```-\
    or\
    -```
    pip3 install Sarvar
    ```-
## How does it work?
The interpreter is in the Engine class.\
Each "Engine" class instances will get a dictionary containing all of data necessary for the commands.
* Structure
  - `{"Command": FunctionInstance}`
The "Engine" class calls a defined command's function with the specified arguments:
* `CommandFunction(token: Token)`
Each function has to be declared by the `Engine.engine_command` static decorator function.\
Example:
```python
@Engine.engine_command(bigger_than=0, lesser_than=float("inf"), macro_immutable=False)
        def printContent(token: Token) :
            token.args.append("Print")
            token.args.append(" ".join(token.privatevars))
```
```macro_immutable: bool``` -> Whether macro expansion should be allowed on command's `token.privatevar`\
\
```bigger_than: int|float``` CLI Arguments should be bigger than `number` for infinite say float("inf")\
```lesser_than``` CLI arguments should be lesser than `number` for infinite say float("inf")
### Tokens
Each token is consisted of:
```
globalvars (dict[str, str]): Global variables accessible throughout execution
privatevars (dict[str, str]): Private variables for current scope
args (list[str]): List of command arguments
macros (dict[str, str]): Defined macro replacements
current_line (int): Current line being executed
all_lines (int): Total number of lines in program
````
`privatevars` is the command line arguments for the specified or detected command\
\
`args` push or append or insert a command to be handeled in the debug list\
\
`macros` list of all macros\
\
`current_line` Current line this command being executed on\
\
`all_lines` All of the lines that is in the current command's execution scope\
\
`globalvars` All of the variables defined by other commands
### Debug list
Commands:
```python
{
    "Warn": self._warn_attr,
    "Error": self._error_attr,
    "Debug": self._debug_attr,
    "Print": self._print_attr,
    "MakeCall": self._make_call_attr,
}
```
Insert a command or key into the `token.args` list to be handeled in the `_handle_debug_list` function
- Structure
  * `["Command-Key from commands", "Arguments for the specified commands"]`
  * Example:
    - ["Warn", "hello!", "Error", "This"]
    - Executes "Warn" function from dict with arguments - argument `"hello!"`
    - Executes "Error" function from dict with arguments - argument `"This"`
### General functions and instance setup
To setup an instance first import the "Sarvar" package
```python
>>> import Sarvar as sr
>>> # Then make an instance by the following structure: Engine (cmd: dict[str, callable], logger: Logger = Logger() #Optional# )
>>> myInstance = sr.Engine({}) # Meaning no commands by default
```
#### Logger class
    Logger class is a class designed for outputing "Engine" outputs
    Such as 'Errors-Warnings and ...'
    How to setup class:
        def_debug = stdout, def_warn = stderr, def_print = stdout, def_err = stderr
        Your output files such as stdout - stderr - ...
        Prints using rich into specified files by specific functions
            def log_error(self, it): rich.print("[red]"+ "ERROR:\t" +str(it)+"[/red]", file=self.error_file)
            def log_warning(self, it): rich.print("[yellow]" + "WARNING:\t" +str(it)+"[/yellow]", file=self.warn_file)
            def log_debug(self, it): rich.print("[blue]"+ "DEBUG:\t" + str(it)+"[/blue]", file=self.debug_file)
            def log_print(self, it): rich.print("[cyan]OUTPUT:\t"+str(it)+"[/cyan]", file =self.print_file)

`add_cmd` -> Adds a new command `(Args: str, callable)`\
\
`remove_cmd` -> Removes a command `(Args: str)`\
\
`push_to_stack` -> Pushes a command to execution stack (`self.commands`) and adds one to the len of execution stack (`self.all_lines`) `(Args: str)`\
\
`interpret` -> interprets the current line (`self.current_line`) `(Args: None)`\
\
`HELPER_InterepetAll` -> interprets until the current line becomes bigger than all of the lines (`self.current_line < self.all_lines`)
`(Args: None)`\
\
`set_flag` -> Sets a specific flag to the specified value `(Args: str, bool)`\
\
`unset_flag` -> Unsets a specific flag `(like the 'not' keyword)` `(Args: str)`\
\
`Flags` -> `[PROPERTY]` Returns the `self.readView`\
\
`get_cmd` -> `[PROPERTY]` Returns the `self.cmd` dictionary
#### Flags
Flags for the `self.interpret` function
* `"_attributename_stop"` -> Raises an error when the attributename gets called `(attributes are functions starting with '_' such as '_error_attr')`
* `"PRN_ShowEvents"` -> Show events for every function with `DebugFunctionIfEnabled` decorator
* `"BOL_HNDLE_DBGLST"` Handle debug list?
* `"SHW_OUTPUT"` Show output `(Do not execute functions marked with ExecuteIfEnabled("SHW_OUTPUT") decorator)`
* `"INTERP_EXEC_EVEN_IF_ERROR"` Execute even If there is a problem with command line arguments or current_line
* `"INTERP_EXEC_EVEN_IF_RAISED"` Do not Raise error If there was an error with command execution? (`True = Do not raise error, False = Raise error`)\
Homepage: https://github.com/ProgrammEverything/Sarvar \
Issues: https://github.com/ProgrammEverything/Sarvar/issues
