class RegionError(Exception):
    """RegionError
    Raises error when the region is not provided correctly
    """
    pass


class LinkLenError(Exception):
    """LinkLenError
    Raises error when the length of a link list is 0
    """
    pass


class NoConnectionError(Exception):
    """NoConnectionError
    Raises when a connection cannot be established to a given ext link
    """
    pass


class PageEmptyError(Exception):
    """PageEmptyError
    Raises when the page has no html content and is empty
    """
    pass


class InvalidPlayerAmount(Exception):
    """InvalidPlayerAmount
    Raises when the number of players in a game is not 10
    """
    pass


class AllNoneError(Exception):
    """AllNoneError
    Raises when all of the data is None
    """
