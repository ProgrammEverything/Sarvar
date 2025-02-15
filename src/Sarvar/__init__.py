from .Engine import Engine
from .error_types import AttrStopExecutionFlag, AttrStopExecution
from .Logger import Logger
from .Token import Token
__all__ = [
    "Engine",
    "AttrStopExecutionFlag",
    "AttrStopExecution",
    "Logger",
    "Token"
]
__package__ = "Sarvar Interpreter"
__version__ = "1.0.0"
__author__  = "Sasan salehi"
__doc__     = "A simple assembly like interpreter implementation. Good for programs which need command shortcuts or command lines for their programs. Not good in speed but good in simplicity."