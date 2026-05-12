import warnings

# Keep output clean in long-running worker processes.
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="You're running the worker with superuser privileges",
)

# Python 3.11: suppress known third-party deprecation warnings.
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    message="ssl.PROTOCOL_TLS is deprecated",
)
