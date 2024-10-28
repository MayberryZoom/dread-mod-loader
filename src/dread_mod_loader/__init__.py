from pathlib import Path
import sys

def is_frozen() -> bool:
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

def get_file_path() -> Path:
    if is_frozen():
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent

def get_data_path() -> Path:
    return get_file_path() / "data"
