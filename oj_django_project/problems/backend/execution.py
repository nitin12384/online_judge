
from . import configs

from .utils import Logger

import os

class ExecutionInfo:
    def __init__(self, memory_usage: int, runtime: int, failed: bool = False,
                 return_code: int = 0, runtime_cap_reached: bool=False,
                 memory_cap_reached: bool=False,
                 message: str = None):
        self.memory_usage = memory_usage
        self.runtime = runtime
        self.failed = failed
        self.return_code = return_code
        self.runtime_cap_reached = runtime_cap_reached
        self.memory_cap_reached = memory_cap_reached
        self.message = message


class Executor:
    def __init__(self, run_args, tlimit: float, memlimit: int):
        # file paths
        self.stdin_file = None
        self.stdout_file = None
        self.stderr_file = None

        self.tlimit = tlimit
        self.memlimit = memlimit

        self.run_args = run_args
    
    def execute() -> ExecutionInfo:
        pass    



