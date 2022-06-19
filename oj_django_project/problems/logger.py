
from datetime import datetime

class Logger() :
    DJANGO_PROJECT_ROOT = '../'
    logFileName = DJANGO_PROJECT_ROOT + 'logs/log.txt'
    verboseLogFileName = DJANGO_PROJECT_ROOT + 'logs/verbose_log.txt'
    
    logFile = open(logFileName, 'a')
    verboseLogFile = open(verboseLogFileName, 'a')

    def log(message : str) :
        Logger.logFile.write('[' + str(datetime.now()) + ']' + message)
