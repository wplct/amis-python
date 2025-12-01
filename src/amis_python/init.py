"""amis-python: generate amis JSON schema in Pythonic way."""

__version__ = "0.1.0"

from .builder import PageBuilder
from .components import *  # 按需暴露

__all__ = ["PageBuilder"]