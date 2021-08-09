class InvalidArgument(Exception):
    def __init__(self, message: str):
        super(InvalidArgument, self).__init__(message)
