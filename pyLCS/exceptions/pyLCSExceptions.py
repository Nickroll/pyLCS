class RegionError(Exception):
    """RegionError
    Raises error when the region is not provided correctly
    """


class LinkLenError(Exception):
    """LinkLenError
    Raises error when the length of a link list is 0
    """


class NoConnectionError(Exception):
    """NoConnectionError
    Raises when a connection cannot be established to a given ext link
    """


class PageEmptyError(Exception):
    """PageEmptyError
    Raises when the page has no html content and is empty
    """
