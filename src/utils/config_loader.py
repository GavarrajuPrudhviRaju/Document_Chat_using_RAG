import os
from pathlib import Path
from src.logger import GLOBAL_LOGGER as log

import yaml


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_config(config_path: str = None):

    env_path = os.getenv("config_path")

    if config_path is None:
        config_path = env_path

    path = Path(config_path)

    if not path.is_absolute():
        path = _project_root()/path

    log.info("current config path", path=path)

    if not path.exists():
        raise FileNotFoundError("config file not found")

    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}
