def parseOperator(value):
    """
    Returns a search operator based on the type of the value to match on.

    :param value: to match in the search.
    :return: operator to use for the type of value.
    """
    if type(value) == str:
        return " LIKE "
    else:
        return "="


def parseValue(value, search: bool = False) -> str:
    """
    Parses a value into a valid value to insert or search in a sqlite database.

    Whenever the search flag is set, % are appended to start and end of a string value to search for all string to
    match the pattern.

    Examples for search=False:
    - 'string' -> '"string"'
    - 4 -> '4'
    Examples for search=True:
    - 'string' -> '"%string%"'
    - 4 -> '4'

    :param search:whether the value should be converted for search or other database tasks.
    :param value: to convert into a valid value for sqlite databases.
    :return: valid value for sqlite databases.
    """
    if type(value) == str:
        search_str = "%" if search else ""
        return '"' + search_str + value + search_str + '"'
    else:
        return str(value)
