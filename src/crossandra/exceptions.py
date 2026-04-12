class CrossandraError(Exception):
    """Base crossandra error"""


class CrossandraTokenizationError(CrossandraError):
    """Unhandled invalid token during tokenization."""


class CrossandraValueError(CrossandraError):
    """An invalid value was used when creating a tokenizer."""
