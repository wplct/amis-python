def ensure_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def merge_dict(base, **overrides):
    data = dict(base)
    for key, value in overrides.items():
        if value is not None:
            data[key] = value
    return data
