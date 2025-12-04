from __future__ import annotations
from pydantic import ConfigDict

def camelize(name: str) -> str:
    """snake_case -> camelCase"""
    parts = name.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])
