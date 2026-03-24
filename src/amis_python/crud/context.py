from typing import Any, Dict, TypedDict


class RenderContext(TypedDict, total=False):
    base_options: Dict[str, Any]
    registry: Any
