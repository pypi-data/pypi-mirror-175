class AMcardsException(Exception):
    """Base exception for all exceptions raised by AMcards"""
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ForbiddenResourceError(AMcardsException):
    """Base exception for when client attempts to access a resource it does not have permission to"""

class ForbiddenTemplateError(ForbiddenResourceError):
    """Template is not owned by clients' user"""

class ForbiddenCampaignError(ForbiddenResourceError):
    """Campaign is not owned by clients' user"""

class ShippingAddressError(AMcardsException, ValueError):
    """Some shipping address fields are missing or invalid"""

class AuthenticationError(AMcardsException):
    """Access token provided to client is unauthorized"""

class InsufficientCreditsError(AMcardsException):
    """Clients' user has insufficient credits"""

class DateFormatError(AMcardsException, ValueError):
    """Invalid format for date"""

class PhoneFormatError(AMcardsException, ValueError):
    """Invalid format for phone number"""

class DuplicateCampaignError(AMcardsException):
    """Duplicate campaign detected"""
