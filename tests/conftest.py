import sys
from pathlib import Path

# Корень репозитория: .../alos-ani-mvp
ROOT_DIR = Path(__file__).resolve().parents[1]

# Гарантируем, что корень проекта в sys.path
root_str = str(ROOT_DIR)
if root_str not in sys.path:
    sys.path.insert(0, root_str)
