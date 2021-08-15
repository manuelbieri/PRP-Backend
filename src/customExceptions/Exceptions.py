class InvalidArgument(Exception):
    def __init__(self, message: str):
        super(InvalidArgument, self).__init__(message)


class AuthenticationFailed(Exception):
    def __init__(self, message: str):
        super(AuthenticationFailed, self).__init__(message)


class InvalidUser(Exception):
    def __init__(self, message: str):
        super(InvalidUser, self).__init__(message)
