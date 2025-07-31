def normalize_path(path):
    if not path:
        return []
    if isinstance(path, dict) and "path" in path:
        return [tuple(p) for p in path["path"] if isinstance(p, (list, tuple)) and len(p) == 2]
    if isinstance(path, (list, tuple)):
        coords = [tuple(p) for p in path if isinstance(p, (list, tuple)) and len(p) == 2]
        if coords:
            return coords
        if isinstance(path[0], list):
            return [tuple(p) for p in path[0] if isinstance(p, (list, tuple)) and len(p) == 2]
    return []
