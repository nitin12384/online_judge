from datetime import datetime

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





