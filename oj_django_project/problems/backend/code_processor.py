# necessary to use abstract class
from .db_handler import get_problem
from . import configs
from .configs import cur_config
from .utils import quote_enclose
from .execution import Executor, ExecutionInfo
from ..models import Problem
from .validation import file_comparer_exact

from overrides import overrides

# can use enum here
class CompilationResult:
    def __init__(self, failed: bool = False, message: str = configs.COMPILED_SUCCESSFULLY_MESSAGE):
        self.failed = failed
        self.message = message


class LanguageProcessorBase:

    def preprocess(self, code_file_full_path: str):
        pass

    # Todo
    def check_security(self, code_file_full_path: str) -> bool:
        return True


    # Override them
    def get_compiler_exec_args(self, code_file_path: str, executable_file_full_path: str) -> list:
        pass

    def get_executable_path(self, executable_dir_path: str, code_file_name_without_extension: str) -> str:
        pass
    
    def get_execute_args(self, executable_file_path: str):
        pass 






    def execute_file_with_io(self, executable_file_path: str, inp_file_path: str,
                             out_file_path: str, runtime_limit: float, memory_limit: int) -> ExecutionInfo:
        
        exec_args = self.get_execute_args(executable_file_path)
        
        return Executor(exec_args, tlimit=runtime_limit, memlimit=memory_limit, 
                 stdin_file=inp_file_path, stdout_file=out_file_path, stderr_file="").execute()
        
    # may generate compiler error
    # returns : executable_file_path, compilation_result
    def create_executable_file(self, code_file_path: str,
                               code_file_name_without_extension: str) -> tuple:
        executable_file_path = self.get_executable_path(cur_config.temp_executable_dir_path,
                                                        code_file_name_without_extension)

        exec_args = self.get_compiler_exec_args(code_file_path, executable_file_path)
        execution_info = Executor(exec_args, tlimit=configs.COMPILATION_TIME_LIMIT,
                                  memlimit=configs.DEFAULT_MEMORY_LIMIT,
                                  stdin_file="", stdout_file="",
                                  stderr_file=cur_config.compilation_stderr_file
                                  ).execute()

        compilation_result = CompilationResult()

        if execution_info.failed:
            compilation_result.failed = True
            compilation_result.message = ""
            # read stderr_file and add to message
            with open(cur_config.compilation_stderr_file, 'r') as err_file:
                for line in err_file.readlines():
                    compilation_result.message += line

        return executable_file_path, compilation_result

    # returns tuple of
    # (verdict : str, verdict_type : int, verdict_detail : str, runtime : float )
    # points of exit : 2
    def process(self, code_file_path: str, code_file_name_without_extension: str,
                num_testcase: int, testcases_dir_path: str, output_dir_path: str,
                runtime_limit: float, memory_limit: int) -> tuple:
        
        # preprocess
        self.preprocess(code_file_path)

        executable_file_path, compilation_result = self.create_executable_file(code_file_path,
                                                                               code_file_name_without_extension)
        # verdict_type : 0 -> AC, 1 -> WA, 2 -> RE, 3 -> TLE, 4 -> MLE, 5 -> CE
        if compilation_result.failed :
            # runtime 0, verdict_type  5, verdict_detail ""
            return "Compilation Error", 5, compilation_result.message, 0

        verdict = "Accepted : Passed #" + str(num_testcase) + " Test Cases."
        verdict_type = 0
        runtime = -1
        memory_usage = -1
        verdict_details = ""

        for testcase_id in range(1, num_testcase + 1):
            # get inp file path
            inp_file_path = get_inp_file_path(testcases_dir_path, testcase_id)
            expected_output_file_path = get_expected_output_file_path(testcases_dir_path, testcase_id)

            # get out file path
            out_file_path = get_output_file_path(output_dir_path, testcase_id)

            # execute
            execution_info = self.execute_file_with_io(executable_file_path, inp_file_path, out_file_path,
                                                       runtime_limit, memory_limit)

            runtime = max(runtime, execution_info.runtime)
            memory_usage = max(memory_usage, execution_info.memory_usage)

            if execution_info.runtime_cap_reached :
                verdict = "TLE on TestCase #" + str(testcase_id) + ". Time Taken " + str(runtime) + "sec."
                verdict_type = 3
                break

            if execution_info.memory_cap_reached :
                verdict = "MLE on TestCase #" + str(testcase_id) + ". Memory Used " + str(memory_usage/(2**20)) + "MB."
                verdict_type = 4
                break
            if execution_info.failed:
                verdict = execution_info.message + " on TestCase #" + str(testcase_id)
                verdict_type = 2
                break

            # compare and update verdict
            if not file_comparer_exact(out_file_path, expected_output_file_path):
                verdict = "Wrong Answer on TestCase #" + str(testcase_id)
                verdict_type = 1
                break

        return verdict, verdict_type, verdict_details, runtime




class CPPLanguageProcessor(LanguageProcessorBase):
    pass


# Todo
class PythonLangaugeProcessor(LanguageProcessorBase):
    def __init__(self):
        # configs like compiler_path
        self.compiler_full_path = cur_config.python_compiler_path
        self.executable_file_extension = ".py"

    @overrides
    def get_compiler_exec_args(self, code_file_path: str, executable_file_full_path: str) -> list:
        # for python we just copy file to executable path
        return [ configs.CONSOLE_FILE_COPIER_1, code_file_path, executable_file_full_path ]

    @overrides
    def get_executable_path(self, executable_dir_path: str, code_file_name_without_extension: str) -> str:
        # dir path should not end with a slash ?
        return executable_dir_path + cur_config.slash + code_file_name_without_extension \
               + self.executable_file_extension

    @overrides
    def get_execute_args(self, executable_file_path: str):
        # for python 
        return [cur_config.python_compiler_path, executable_file_path]

    

class CPP14LanguageProcessor(CPPLanguageProcessor):

    def __init__(self):
        # configs like compiler_path
        self.compiler_full_path = cur_config.cpp_compiler_path
        self.executable_file_extension = ".out"

    @overrides
    def get_compiler_exec_args(self, code_file_path: str, executable_file_full_path: str) -> list:
        return [ self.compiler_full_path, code_file_path, "-o", executable_file_full_path]

    @overrides
    def get_executable_path(self, executable_dir_path: str, code_file_name_without_extension: str) -> str:
        # dir path should not end with a slash ?

        return executable_dir_path + cur_config.slash + code_file_name_without_extension \
               + self.executable_file_extension

    @overrides
    def get_execute_args(self, executable_file_path: str):
        # for c++ executables
        return [executable_file_path]

    

LanguageProcessorMapping = {
    1: CPP14LanguageProcessor(),
    2: PythonLangaugeProcessor()
}


def get_language_processor(language_id: int) -> LanguageProcessorBase:
    assert type(language_id) == int
    return LanguageProcessorMapping[language_id]


def get_testcases_dir_path(problem: Problem) -> str:
    return cur_config.problem_data_dir_path + \
           problem.data_dir_path + cur_config.testcase_dir_relative_path


def get_output_dir_path() -> str:
    return cur_config.temp_out_data_dir_path


def get_inp_file_path(testcases_dir_path: str, testcase_id: int) -> str:
    return testcases_dir_path + cur_config.slash + "inp_" + str(testcase_id) + ".txt"


def get_expected_output_file_path(testcases_dir_path: str, testcase_id: int) -> str:
    return testcases_dir_path + cur_config.slash + "out_" + str(testcase_id) + ".txt"


def get_output_file_path(output_dir_path: str, testcase_id: int = 0) -> str:
    return output_dir_path + cur_config.slash + "gen_out_" + str(testcase_id) + ".txt"


# return verdict, verdict_type, runtime
def process(code_file_full_path: str, language_id: int,
            submission_id: int, problem_id: int, code_file_name_without_extension: str) -> tuple:
    
    language_processor = get_language_processor(language_id)
    # Task : preprocess
    language_processor.preprocess(code_file_full_path)

    # Task : Initial security checks etc.
    if not language_processor.check_security(code_file_full_path):
        return configs.SECURITY_CHECK_FAILED_VERDICT,5,0

    # Task : get input path, output path ..
    problem = get_problem(problem_id)
    num_testcases = problem.num_testcases
    testcases_dir_path = get_testcases_dir_path(problem)
    output_dir_path = get_output_dir_path()
    runtime_limit = problem.time_limit # float
    memory_limit = configs.DEFAULT_MEMORY_LIMIT  # bytes , by default

    # Task : compile and run and generate output
    # match output of testcase i, before running for testcase i+1
    # and get the verdict
    return language_processor.process(code_file_full_path, code_file_name_without_extension,
                                      num_testcases, testcases_dir_path, output_dir_path,
                                      runtime_limit, memory_limit)
