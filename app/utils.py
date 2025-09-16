from markupsafe import escape
import bleach

def sanitize_input(input_data):
    """Sanitize user input to prevent XSS"""
    if isinstance(input_data, str):
        # First escape HTML, then clean with bleach
        escaped = escape(input_data)
        return bleach.clean(escaped, strip=True)
    elif isinstance(input_data, dict):
        return {k: sanitize_input(v) for k, v in input_data.items()}
    elif isinstance(input_data, list):
        return [sanitize_input(item) for item in input_data]
    return input_data
