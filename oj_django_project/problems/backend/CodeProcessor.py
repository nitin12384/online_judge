
from .DatabaseHandler import get_problem

class LanguageProcessorBase:
    pass


class CPPLanguageProcessor(LanguageProcessorBase):
    pass


class CPP14LanguageProcessor(CPPLanguageProcessor):
    pass


LanguageProcessorMapping = {
    1: CPP14LanguageProcessor(),
}


def get_language_processor(language_id: int) -> LanguageProcessorBase:
    return LanguageProcessorMapping[language_id]


def process(code_file_full_path: str, language_id: int,
            submission_id: int, problem_id: int) -> str:
    # return verdict
    language_processor = get_language_processor(language_id)
    # Task : preprocess

    # Task : Initial security checks etc.

    # Task : get input path, output path ..

    # Task : compile and run and generate output
    # match output of testcase i, before running for testcase i+1
    # and get the verdict

    problem = get_problem(problem_id)

    #

    pass
