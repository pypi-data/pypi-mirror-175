"""Integração - Bling - Exceptions."""


class EndOfPaginationError(Exception):
    """End of pagination error."""

    pass


class APIError(Exception):
    """API error."""

    pass


class IntegrationError(Exception):
    """Integration error."""

    pass


class AlreadySavedError(Exception):
    """Order already saved error."""

    pass
