# custom_exceptions.py
class NotFoundException(Exception):
    """Raised when a video is not found in the database."""
    pass

class InvalidURLFormatException(Exception):
    """Raised when a video format is invalid or unsupported."""
    pass

class AlreadyExistsException(Exception):
    """Raised when a resource already exists in the database."""
    pass