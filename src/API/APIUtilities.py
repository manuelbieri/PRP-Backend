import datetime
import os.path

import customExceptions.Exceptions as Exceptions


def checkAPIArgs(*args) -> None:
    for i in args:
        writeLogs(i)
        if i is None:
            raise Exceptions.InvalidArgument("None Argument is not valid")


def checkDatabaseID(*args):
    for number in args:
        writeLogs(number)
        if type(number) is not int:
            raise Exceptions.InvalidArgument('Invalid ID as argument')
        elif number <= 0:
            raise Exceptions.InvalidArgument('Invalid ID as argument')


def writeLogs(message: str):
    path: str = os.path.dirname(__file__) + '/log/api.log'
    assert os.path.isfile(path)
    time: datetime.date = datetime.date.today()
    time_string: str = time.strftime('%d-%m-%y | %H:%M:%S => ')
    with open(path, 'a') as log:
        log.write(time_string + message)
    log.close()
