
from . import configs

from .utils import Logger

import os


class ExecutionCap:
    def __init__(self,
                 runtime_cap: int,
                 memory_cap: int):
        self.memory_cap = memory_cap
        self.runtime_cap = runtime_cap

# ugly global var
default_execution_cap = ExecutionCap(5000, 500)


class ExecutionInfo:
    def __init__(self, memory_usage: int, runtime: int, failed: bool = False,
                 return_code: int = 0, message: str = configs.EXECUTED_SUCCESSFULLY_MESSAGE):
        self.memory_usage = memory_usage
        self.runtime = runtime
        self.failed = failed
        self.return_code = return_code
        self.message = message


# Todo
def run_command(command: str, execution_cap: ExecutionCap=default_execution_cap) -> ExecutionInfo:
    # the limit is 8191 character .
    if len(command) >= configs.COMMAND_LENGTH_LIMIT:
        Logger.log("Command is too big " + command)
        return None

    Logger.log("Executing command : " + command)
    ret_val = os.system(command)
    Logger.log("ret_val of command : " + str(ret_val))
    execution_info = ExecutionInfo(0,0)
    if ret_val != 0:
        execution_info.failed = True
        execution_info.message = "Failed"

    return execution_info

