class AvatarNotFound(Exception):
    """
    Exception raised when avatar cannot be found
    """
    pass

class AvatarConversionFailure(Exception):
    """
    Exception raised when avatar cannot be converted from raw to known format
    """
    pass
