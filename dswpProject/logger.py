from datetime import datetime

class Logger:
    def __init__(self):
        self.DEFAULT = '\033[0m'
        self.WARNING = '\033[93m'
        self.SUCCESS = '\033[92m'
        self.ERROR = '\033[91m'
    
    def date(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def print(self, text):
        print(text)

    def message(self, text):
        print(self.date() + ' [INFO] ' + text)

    def success(self, text):
        print(self.SUCCESS + self.date() + ' [SUCCESS] ' +  text + self.DEFAULT)

    def error(self, text):
        print(self.ERROR + self.date() + ' [ERROR] ' + text + self.DEFAULT)

    def warning(self, text):
        print(self.WARNING + self.date() + ' [WARNING] ' + text + self.DEFAULT)