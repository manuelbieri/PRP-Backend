import customExceptions.Exceptions as Exceptions


def checkAPIArgs(*args) -> None:
    for i in args:
        if i is None:
            raise Exceptions.InvalidArgument("None Argument is not valid")


def checkDatabaseID(*args):
    for number in args:
        if type(number) is not int:
            raise Exceptions.InvalidArgument('Invalid ID as argument')
        elif number <= 0:
            raise Exceptions.InvalidArgument('Invalid ID as argument')
