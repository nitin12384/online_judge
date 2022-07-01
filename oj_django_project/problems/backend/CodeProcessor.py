
from .DatabaseHandler import get_problem
from . import configs

from ..models import Problem

class LanguageProcessorBase:
    @staticmethod
    def preprocess(code_file_full_path: str):
        pass

    @staticmethod
    def check_security(code_file_full_path: str) -> bool:
        return True


class CPPLanguageProcessor(LanguageProcessorBase):
    pass


class CPP14LanguageProcessor(CPPLanguageProcessor):
    pass


LanguageProcessorMapping = {
    1: CPP14LanguageProcessor(),
}


def get_language_processor(language_id: int) -> LanguageProcessorBase:
    return LanguageProcessorMapping[language_id]

def get_testcases_dir_path(problem: Problem) -> str:
    return configs.PROBLEM_DATA_BASE_PATH + \
            problem.data_dir_path + configs.TESTCASES_DIR


def get_output_dir_path() -> str:
    configs.SUBMISSION_DATA_BASE_PATH


def process(code_file_full_path: str, language_id: int,
            submission_id: int, problem_id: int) -> str:
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

    # Task : compile and run and generate output
    # match output of testcase i, before running for testcase i+1
    # and get the verdict


    #

    pass
