
from datetime import datetime

class Logger() :
    logFileName = 'log.txt'
    verboseLogFileName = 'verbose_log.txt'
    
    logFile = open(logFileName, 'a')
    verboseLogFile = open(verboseLogFileName, 'a')

    def log(message : str) :
        Logger.logFile.write('[' + str(datetime.now()) + ']' + message)
