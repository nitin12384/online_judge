# necessary to use abstract class
from abc import abstractmethod

from .db_handler import get_problem
from . import configs
from .utils import quote_enclose
from .execution import run_command, ExecutionInfo, ExecutionCap
from ..models import Problem
from .validation import file_comparer_exact


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

    # Override it
    # Like abstract method
    # returns the output file full
    def create_executable_file(self, code_file_full_path: str,
                               code_file_name_without_extension: str) -> tuple:
        pass


class CPPLanguageProcessor(LanguageProcessorBase):
    pass


class CPP14LanguageProcessor(CPPLanguageProcessor):

    def __init__(self):
        # configs like compiler_path
        self.compiler_full_path = configs.cur_config.cpp_compiler_path
        self.executable_file_extension = ".out"

    def get_executable_path(self, executable_dir_path: str, code_file_name_without_extension: str) -> str:
        # dir path should not end with a slash ?

        return executable_dir_path + configs.SLASH + code_file_name_without_extension \
               + self.executable_file_extension

    # may generate compiler error
    # returns : executable_file_path, compilation_result
    def create_executable_file(self, code_file_path: str,
                               code_file_name_without_extension: str) -> tuple:
        executable_file_path = self.get_executable_path(configs.TEMP_EXECUTABLE_DIR_PATH,
                                                        code_file_name_without_extension)

        command = self.get_compiler_command(code_file_path, executable_file_path)
        execution_info = run_command(command)

        compilation_result = CompilationResult()
        if execution_info.failed:
            compilation_result.failed = True
            compilation_result.message = "Compilation Failed . Message : \n" + execution_info.message

        return executable_file_path, compilation_result

    def get_compiler_command(self, code_file_path: str, executable_file_full_path: str) -> str:
        return self.compiler_full_path + configs.SPACE + \
               quote_enclose(code_file_path) + " -o " + quote_enclose(executable_file_full_path)

    @staticmethod
    def get_execute_command(executable_file_path: str, inp_file_path: str,
                            out_file_path: str):
        # for c++ executables
        return "type " + quote_enclose(inp_file_path) + \
            " | " + quote_enclose(executable_file_path) + \
            " > " + out_file_path

    def execute_file_with_io(self, executable_file_path: str, inp_file_path: str,
                             out_file_path: str, runtime_limit: int, memory_limit: int) -> ExecutionInfo:
        command = self.get_execute_command(executable_file_path, inp_file_path, out_file_path)
        return run_command(command, ExecutionCap(runtime_limit, memory_limit))

    def process(self, code_file_path: str, code_file_name_without_extension: str,
                num_testcase: int, testcases_dir_path: str, output_dir_path: str,
                runtime_limit: int, memory_limit: int) -> tuple:
        # preprocess
        self.preprocess(code_file_path)

        # security check
        if not self.check_security(code_file_path):
            return configs.SECURITY_CHECK_FAILED_VERDICT

        executable_file_path, compilation_result = self.create_executable_file(code_file_path,
                                                                               code_file_name_without_extension)
        # verdict_type : 0 -> AC, 1 -> WA, 2 -> RE, 3 -> TLE, 4 -> MLE, 5 -> CE
        if compilation_result.failed :
            # runtime 0
            # verdict_type  5
            return "Compilation Error", 5, 0

        verdict = "Accepted : Passed #" + str(num_testcase) + " Test Cases."
        verdict_type = 0
        runtime = -1

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

            if execution_info.runtime_cap_reached :
                verdict = "TLE on TestCase #" + str(testcase_id)
                verdict_type = 3
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

        return verdict, verdict_type, runtime


LanguageProcessorMapping = {
    1: CPP14LanguageProcessor(),
}


def get_language_processor(language_id: int) -> LanguageProcessorBase:
    assert type(language_id) == int
    return LanguageProcessorMapping[language_id]


def get_testcases_dir_path(problem: Problem) -> str:
    return configs.cur_config.problem_data_dir_path + \
           problem.data_dir_path + configs.TESTCASES_DIR_RELATIVE_PATH


def get_output_dir_path() -> str:
    return configs.cur_config.temp_out_data_dir_path


def get_inp_file_path(testcases_dir_path: str, testcase_id: int) -> str:
    return testcases_dir_path + r"/inp_" + str(testcase_id) + ".txt"


def get_expected_output_file_path(testcases_dir_path: str, testcase_id: int) -> str:
    return testcases_dir_path + r"/out_" + str(testcase_id) + ".txt"


def get_output_file_path(output_dir_path: str, testcase_id: int = 0) -> str:
    return output_dir_path + r"/gen_out_" + str(testcase_id) + ".txt"


def process(code_file_full_path: str, language_id: int,
            submission_id: int, problem_id: int, code_file_name_without_extension: str) -> tuple:
    # return verdict, runtime
    language_processor = get_language_processor(language_id)
    # Task : preprocess
    language_processor.preprocess(code_file_full_path)

    # Task : Initial security checks etc.
    if not language_processor.check_security(code_file_full_path):
        return configs.SECURITY_CHECK_FAILED_VERDICT

    # Task : get input path, output path ..
    problem = get_problem(problem_id)
    num_testcases = problem.num_testcases
    testcases_dir_path = get_testcases_dir_path(problem)
    output_dir_path = get_output_dir_path()
    runtime_limit = problem.time_limit
    memory_limit = configs.DEFAULT_MEMORY_LIMIT  # MB , by default

    # Task : compile and run and generate output
    # match output of testcase i, before running for testcase i+1
    # and get the verdict
    return language_processor.process(code_file_full_path, code_file_name_without_extension,
                                      num_testcases, testcases_dir_path, output_dir_path,
                                      runtime_limit, memory_limit)
