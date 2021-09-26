# -*- coding: utf-8 -*-

import logging.config
import os
from pathlib import Path

import yaml

from resources.properties import LOGS_FOLDER, LOGS_LEVEL, LOGS_MODE

file_path = Path(__file__).absolute()
root_folder = file_path.parent.parent
path_log_folder = Path(root_folder).joinpath(LOGS_FOLDER)

if not os.path.exists(path_log_folder):
    try:
        os.mkdir(path_log_folder)
    except FileExistsError:
        print(f"The logs directory already exists.")
    except OSError:
        print(f"Creation of the log directory '{path_log_folder}' failed")

path_log_config_file = Path(root_folder).joinpath('resources').joinpath('log.yaml')

if os.path.exists(path_log_config_file):
    if os.path.isfile(path_log_config_file):
        with open(path_log_config_file, 'rt') as config_file:
            config = yaml.safe_load(config_file.read())
            logging.config.dictConfig(config)
    else:
        print(f"The path to the log configuration file must be a file not a directory: {path_log_config_file}")
else:
    print(f"The path to the log configuration file do not exist: {path_log_config_file}")

logger = logging.getLogger(LOGS_MODE)
logger.setLevel(LOGS_LEVEL)
