"""Utilities for Python JSON Logger"""

### IMPORTS
### ============================================================================
## Future
from __future__ import annotations

## Standard Library
import importlib.util

## Installed

## Application
from .exception import MissingPackageError


### FUNCTIONS
### ============================================================================
def package_is_available(
    name: str, *, throw_error: bool = False, extras_name: str | None = None
) -> bool:
    """Determine if the given package is available for import.

    Args:
        name: Import name of the package to check.
        throw_error: Throw an error if the package is unavailable.
        extras_name: Extra dependency name to use in `throw_error`'s message.

    Raises:
        MissingPackageError: When `throw_error` is `True` and the return value would be `False`

    Returns:
        If the package is available for import.
    """
    try:
        available = importlib.util.find_spec(name) is not None
    except ModuleNotFoundError as exc:
        # A dotted import also fails when one of its parent packages is missing.
        # Preserve errors from unrelated dependencies imported by an existing parent.
        if exc.name is None or not (name == exc.name or name.startswith(exc.name + ".")):
            raise
        available = False

    if not available and throw_error:
        raise MissingPackageError(name, extras_name)

    return available
