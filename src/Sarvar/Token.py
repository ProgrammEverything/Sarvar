from dataclasses import dataclass, field
@dataclass
class Token:
    """
    A data class representing the current state of the interpreter.
    
    Attributes:
        globalvars (dict[str, str]): Global variables accessible throughout execution
        privatevars (dict[str, str]): Private variables for current scope
        args (list[str]): List of command arguments
        macros (dict[str, str]): Defined macro replacements
        current_line (int): Current line being executed
        all_lines (int): Total number of lines in program
    """
    globalvars: dict[str, str] = field(default_factory=dict)
    privatevars: list[str] = field(default_factory=list[str])
    args: list[str] = field(default_factory=list)
    macros: dict[str,str] = field(default_factory=dict)
    current_line: int = field(default_factory=int)
    all_lines: int = field(default_factory=int)