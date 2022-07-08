
from . import configs

class ExecutionCap:
    def __init__(self,
                 runtime_cap: int,
                 memory_cap: int):
        self.memory_cap = memory_cap
        self.runtime_cap = runtime_cap


class ExecutionInfo:
    def __init__(self, memory_usage: int, runtime: int, failed: bool = False,
                 return_code: int = 0, message: str = configs.EXECUTED_SUCCESSFULLY_MESSAGE):
        self.memory_usage = memory_usage
        self.runtime = runtime
        self.failed = failed
        self.return_code = return_code
        self.message = message


# Todo
def run_command(command: str, execution_cap: ExecutionCap) -> ExecutionInfo:
    # the limit is 8191 character .
    return ExecutionInfo(0, 0)

