from pathlib import Path


def load_res(name: str) -> str:
    mod_path = Path(__file__).parent
    path = str(mod_path.parent) + '\\res\\' + name
    return path