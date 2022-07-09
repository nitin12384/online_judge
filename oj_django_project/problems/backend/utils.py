from datetime import datetime

from ..models import Problem, Language, ProblemLanguageRelation

from . import configs



class LogginMethods:
    LOG_STDOUT = 1


class Logger:
    def_logging_method = LogginMethods.LOG_STDOUT

    DJANGO_PROJECT_ROOT = '../../'
    logFileName = DJANGO_PROJECT_ROOT + 'logs/log.txt'
    verboseLogFileName = DJANGO_PROJECT_ROOT + 'logs/verbose_log.txt'

    # logFile = open(logFileName, 'a')
    # verboseLogFile = open(verboseLogFileName, 'a')

    def __init__(self):
        self.logging_method = 1

    @staticmethod
    def log(msg):
        # msg could be str or may not be ...
        if Logger.def_logging_method == LogginMethods.LOG_STDOUT:
            print('[' + str(datetime.now()) + '] ' + msg)




# global properties
def quote_enclose(s: str) -> str:
    return "\"" + s + "\""


def to_window_slash(s: str) -> str:
    assert s != None
    res = ""
    for i in range(0, len(s)):
        if s[i] == '/':
            res += '\\'
        else:
            res += s[i]
    return res


def read_br_seperated_file(inp_file) -> str:
    res = ""
    lines_list = inp_file.readlines()
    for line in lines_list:
        res += line + "<br/>"

    return res


"""
absolute path = "C:\\....\data\problems_data"
data_dir_path = "\1"

/desc.txt : description of the file
/input.txt : input details
/output.txt : output details
/constraints.txt : constraints details
/examples.txt : constraints details

/testcases/ : directory of test_cases, in which we have input/output files
inp_1.txt, inp_2.txt, ....inp_k.txt, where k is 'num_testcases'
out_1.txt, out_2.txt, ...
"""


def get_problem_detailed_context(problem: Problem) -> dict:
    data_dir = None

    # get the data directory
    if configs.ENVIRONMENT == configs.ENV_WINDOWS1:
        data_dir = configs.PROBLEM_DATA_BASE_PATH + to_window_slash(problem.data_dir_path)

    assert data_dir != None

    description_file_path = data_dir + "/description.txt"
    input_file_path = data_dir + "/input.txt"
    output_file_path = data_dir + "/output.txt"
    constraints_file_path = data_dir + "/constraints.txt"
    examples_file_path = data_dir + "/examples.txt"

    file_paths = [description_file_path, input_file_path, output_file_path,
                  constraints_file_path, examples_file_path]

    if configs.ENVIRONMENT == configs.ENV_WINDOWS1:
        # convert slash acc. to windows
        file_paths = [to_window_slash(s) for s in file_paths]

    files = [open(s, "r") for s in file_paths]
    file_data = [f.read() for f in files]

    # close files
    for f in files:
        f.close()

    plr_set = problem.problemlanguagerelation_set.all()

    languages = []
    languages_str = ""

    for plr in plr_set:
        language_id = plr.language_id
        cur_language = Language.objects.get(pk=language_id)
        languages.append(cur_language)
        languages_str += cur_language.name + ", "

    return {
        'problem': problem,

        'description': file_data[0],
        'input': file_data[1],
        'output': file_data[2],
        'constraints': file_data[3],
        'examples': file_data[4],
        'languages': languages,
        'languages_str': languages_str,

    }
