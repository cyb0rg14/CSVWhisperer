import os
from pathlib import Path

CURRENT_PATH = Path.cwd()
DATASETS = os.listdir(f"{CURRENT_PATH}/datasets")