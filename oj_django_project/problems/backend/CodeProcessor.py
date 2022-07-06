# necessary to use abstract class
from abc import abstractmethod

from .DatabaseHandler import get_problem
from . import configs
from .utils import command_runner
from ..models import Problem
from .validation import file_comparer_exact


class CompilationResult:
    def __init__(self, failed: bool = False, message: str = configs.COMPILED_SUCCESSFULLY_MESSAGE):
        self.failed = failed
        self.message = message


class ExecutionResult:
    def __init__(self, runtime: int = 0, failed: bool = False, message: str = "Successfully Executed"):
        self.failed = failed
        self.runtime = runtime
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
                               code_file_name_without_extension: str) -> tuple(str, CompilationResult):
        pass


class CPPLanguageProcessor(LanguageProcessorBase):
    pass


class CPP14LanguageProcessor(CPPLanguageProcessor):

    # Todo
    def __init__(self):
        # configs like compiler_path
        self.compiler_full_path = ""
        self.executable_file_extension = ".out"

    # Todo : test
    def get_executable_path(self, executable_dir_path: str, code_file_name_without_extension: str) -> str:
        # dir path should not end with a slash ?

        return executable_dir_path + configs.SLASH + code_file_name_without_extension \
               + self.executable_file_extension

    # Todo
    # may generate compiler error
    def create_executable_file(self, code_file_full_path: str,
                               code_file_name_without_extension: str) -> tuple(str, str):
        pass

    # Todo
    def get_compiler_command(self, code_file_full_path: str, executable_file_full_path: str) -> str:
        pass

    # Make command for
    # Todo
    def get_execute_command(self, executable_file_full_path: str, inp_file_full_path: str,
                            out_file_full_path: str):
        pass

    def execute_file_with_io(self, executable_file_full_path: str, inp_file_full_path: str,
                             out_file_full_path: str) -> ExecutionResult:
        pass

    # Todo : test
    def process(self, code_file_path: str, code_file_name_without_extension: str,
                num_testcase: int, testcases_dir_path: str, output_dir_path) -> str:
        # preprocess
        self.preprocess(code_file_path)

        # security check
        if not self.check_security(code_file_path):
            return configs.SECURITY_CHECK_FAILED_VERDICT

        executable_file_path, compilation_result = self.create_executable_file(code_file_path,
                                                                               code_file_name_without_extension)

        if compilation_result.failed :
            return "Compilation Error"

        verdict = "Accepted : Passed #" + str(num_testcase) + " Test Cases."

        for testcase_id in range(1, num_testcase + 1):
            # get inp file path
            inp_file_path = get_inp_file_path(testcases_dir_path, testcase_id)
            expected_output_file_path = get_expected_output_file_path(testcases_dir_path, testcase_id)

            # get out file path
            out_file_path = get_output_file_path(output_dir_path, testcase_id)

            # execute
            execution_result = self.execute_file_with_io(executable_file_path, inp_file_path, out_file_path)

            # Check result
            # Todo : confirm
            if execution_result.failed:
                verdict = execution_result.message + "on TestCase #" + str(testcase_id)
                break

            # compare and update verdict
            # Todo : test
            if not file_comparer_exact(out_file_path, expected_output_file_path):
                verdict = "Wrong Answer on TestCase #" + str(testcase_id)
                break

        return verdict


LanguageProcessorMapping = {
    1: CPP14LanguageProcessor(),
}


def get_language_processor(language_id: int) -> LanguageProcessorBase:
    return LanguageProcessorMapping[language_id]


def get_testcases_dir_path(problem: Problem) -> str:
    return configs.PROBLEM_DATA_BASE_PATH + \
           problem.data_dir_path + configs.TESTCASES_DIR


def get_output_dir_path() -> str:
    return configs.TEMP_OUTPUT_DATA_PATH


# Todo : Confirm
def get_inp_file_path(testcases_dir_path: str, testcase_id: int) -> str:
    return testcases_dir_path + r"/inp_" + str(testcase_id) + ".txt"


# Todo : Confirm
def get_expected_output_file_path(testcases_dir_path: str, testcase_id: int) -> str:
    return testcases_dir_path + r"/out_" + str(testcase_id) + ".txt"


# Todo : Confirm
def get_output_file_path(output_dir_path: str, testcase_id: int = 0) -> str:
    return output_dir_path + r"/gen_out_" + str(testcase_id) + ".txt"


# Todo : Confirm
def process(code_file_full_path: str, language_id: int,
            submission_id: int, problem_id: int, code_file_name_without_extension: str) -> str:
    # return verdict
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

    # Task : compile and run and generate output
    # match output of testcase i, before running for testcase i+1
    # and get the verdict
    return language_processor.process(code_file_full_path, code_file_name_without_extension,
                                      num_testcases, testcases_dir_path, output_dir_path)
