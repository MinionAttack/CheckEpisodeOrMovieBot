# -*- coding: utf-8 -*-

import logging.config
import os

import yaml

from resources.properties import LOGS_FOLDER, LOGS_MODE

path_log_folder = os.path.join('.', LOGS_FOLDER)

if not os.path.exists(path_log_folder):
    try:
        os.mkdir(path_log_folder)
    except OSError:
        print(f"Creation of the log directory '{path_log_folder}' failed")
else:
    path_critical_log_file = os.path.join(path_log_folder, 'critical.log')
    path_debug_log_file = os.path.join(path_log_folder, 'debug.log')
    path_errors_log_file = os.path.join(path_log_folder, 'errors.log')
    path_info_log_file = os.path.join(path_log_folder, 'info.log')
    path_warn_log_file = os.path.join(path_log_folder, 'warn.log')

    log_files = [path_critical_log_file, path_debug_log_file, path_errors_log_file, path_info_log_file, path_warn_log_file]

    for log_file in log_files:
        if not os.path.exists(log_file):
            created_file = None
            try:
                created_file = open(log_file, 'r')
            except (IOError, EOFError) as error:
                print(f"Unable to create log file: {log_file}")
                print(error)
            finally:
                if created_file is not None:
                    created_file.close()


path_log_config_file = os.path.join('.', 'resources', 'log.yaml')

if os.path.exists(path_log_config_file):
    if os.path.isfile(path_log_config_file):
        with open(path_log_config_file, 'r') as config_file:
            config = yaml.safe_load(config_file.read())
            logging.config.dictConfig(config)
            config_file.close()
    else:
        print(f"The path to the log configuration file must be a file not a directory: {path_log_config_file}")
else:
    print(f"The path to the log configuration file do not exist: {path_log_config_file}")

logger = logging.getLogger(LOGS_MODE)

