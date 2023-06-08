
from . import configs

from .utils import Logger

import os
import psutil
import threading
import subprocess
import time
import datetime

class ExecutionInfo:
    def __init__(self, memory_usage: int = -1, runtime: int = -1, failed: bool = True,
                 return_code: int = 0, runtime_cap_reached: bool=False,
                 memory_cap_reached: bool=False,
                 message: str = None):
        self.memory_usage           = memory_usage # peak memory usage
        self.runtime                = runtime
        self.failed                 = failed
        self.return_code            = return_code
        self.runtime_cap_reached    = runtime_cap_reached
        self.memory_cap_reached     = memory_cap_reached
        self.message                = message # when code is failed, but time/memory limit are not exceeded
    def __str__(self):
        return "memory_usage"   + str(self.memory_usage       ) + \
              "B = " + str(self.memory_usage/(2**20)) + "MB" \
        " runtime"               + str(self.runtime            ) + \
        " failed"                + str(self.failed             ) + \
        " return_code"           + str(self.return_code        ) + \
        " runtime_cap_reached"   + str(self.runtime_cap_reached) + \
        " memory_cap_reached"    + str(self.memory_cap_reached ) + \
        " message"               + str(self.message            )


class Executor:
    def_memchecker_period = 0.1 # seconds
    @staticmethod
    def memcheck_worker(pid : int, memlim_bytes : int, check_delay_sec: float, result : ExecutionInfo):
        proc_obj = psutil.Process(pid)
        result.memory_cap_reached = False
        result.memory_usage = 0

        while proc_obj.is_running() :

            mem_used = proc_obj.memory_info().rss
            result.memory_usage = max(mem_used, result.memory_usage)
            if mem_used > memlim_bytes :
                Logger.log("Memory Limit Exceeded")
                # need to somehow also return the information to thread starter
                result.memory_cap_reached = True
                proc_obj.kill()
            time.sleep(check_delay_sec)
        
        result.memory_usage

    
    def __init__(self, exec_args : list, tlimit: float, memlimit: int,
                 stdin_file  = None,
                 stdout_file = None,
                 stderr_file = None
                 ):
        # file paths
        self.stdin_file  = stdin_file 
        self.stdout_file = stdout_file
        self.stderr_file = stderr_file

        self.tlimit = tlimit
        self.memlimit = memlimit

        self.exec_args = exec_args
    
    def init_io(self):
        self.inp,self.out,self.error = None, None, None 
        if self.stdin_file :
            self.inp = open(self.stdin_file, 'r')
        if self.stdout_file:
            self.out = open(self.stdout_file, 'w')
        if self.stderr_file:
            self.error = open(self.stderr_file, 'w')
    
    def close_io(self):
        if self.stdin_file:
            self.inp.close()
        if self.stdout_file:
            self.out.flush()
            self.out.close()
        if self.stderr_file:
            self.error.flush()
            self.error.close()
    
    def execute(self) -> ExecutionInfo:

        self.init_io()

        Logger.log("Executing process with args : ", self.exec_args)

        proc = subprocess.Popen(self.exec_args, stdin=self.inp, stdout=self.out, stderr=self.error)
        result = ExecutionInfo()

        Logger.log("Process created")

        memchecker_thread = threading.Thread(target=Executor.memcheck_worker,
        args=[proc.pid, self.memlimit, Executor.def_memchecker_period,result])
        memchecker_thread.start()

        Logger.log("memcheck_thread started")

        t_start = datetime.datetime.now()

        # Time Limit checker code
        try:
            proc.wait(timeout=self.tlimit)
        except subprocess.TimeoutExpired:
            Logger.log("Time Limit Exceed while executing.")
            proc.kill()
            result.runtime_cap_reached = True
        
        # Join memchecker_thread
        memchecker_thread.join()

        Logger.log("Process execution done")

        t_end = datetime.datatime.now()
        result.runtime = int ( (t_end - t_start).total_seconds()*1000 ) # msecs

        # Close IO Files
        self.close_io()

        # Finalize result
        self.return_code = proc.poll()

        if self.return_code != 0:
            result.failed = True 
            result.message = configs.RUNTIME_ERROR_MESSAGE

        result.failed |= result.memory_cap_reached | result.runtime_cap_reached
        
        Logger.log("Execution Result : ", result)

        return result





