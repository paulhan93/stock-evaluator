from typing import Any, Union

def safe_division(a: Any, b: Any) -> Union[float, str]:
    """Safely perform division, returning 'N/A' if invalid"""
    try:
        if a is None or b is None or b == 0:
            return "N/A"
        return a / b
    except Exception:
        return "N/A" 