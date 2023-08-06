#!/usr/bin/env python

# (C) Copyright 2022 United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration. All Rights Reserved.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.

# --------------------------------------------------------------------------------------------------


import argparse
import os
import requests
import yaml

from jedi_bundle.clone_jedi_bundle import clone_jedi
from jedi_bundle.configure_jedi_bundle import configure_jedi
from jedi_bundle.make_jedi_bundle import make_jedi

from jedi_bundle.config.config import return_config_path
from jedi_bundle.utils.file_system import prompt_and_remove_file
from jedi_bundle.utils.logger import Logger, colors
from jedi_bundle.utils.yaml import load_yaml


# --------------------------------------------------------------------------------------------------


def jedi_bundle():

    # Arguments
    # ---------
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('tasks_and_config', type=str, nargs='*', default=None,
                        help='There are two ways of running jedi_bundle. Either with no arguments '
                             'or two (or more) arguments. \nWhen no argument is provided the code '
                             'will generate the config file build.yaml in the working \ndirectory '
                             'and then exit. When two (or more) arguments are passed the final '
                             'argument must be the \npath to the configuration file. The '
                             'proceeding arguments are the choice of task(s) to run.'
                             '\n\nThe valid tasks are \'Clone\', \'Configure\', \'Build\' and '
                             '\'All\', where \'All\' runs all of the above. \nTasks names are case '
                             'insensitive. ' +
                             '\n\nExamples:\n' +
                             '  jedi_bundle                             (Generate config) \n' +
                             '  jedi_bundle All build.yaml              (All tasks) \n' +
                             '  jedi_bundle all build.yaml              (All tasks) \n' +
                             '  jedi_bundle Clone build.yaml            (Clone task) \n'
                             '  jedi_bundle Clone Configure build.yaml  (Clone & Configure task)\n')

    # Create the logger
    logger = Logger('JediBundle')

    # Parse input string
    args = parser.parse_args()
    tasks_and_config = args.tasks_and_config

    # If there are no arguments create build.yaml and exit
    if tasks_and_config == []:

        # Prepare the configuration from default
        # --------------------------------------
        config_file_name = 'build.yaml'
        internal_config_file = os.path.join(return_config_path(), config_file_name)
        internal_config_dict = load_yaml(logger, internal_config_file)

        # Set current directory for source code
        internal_config_dict['clone_options']['path_to_source'] = os.getcwd()

        # Set default build directory
        build_dir = os.path.join(os.getcwd(), 'build')

        # Guess the platform
        hostname = os.uname()[1].lower()
        supported_platforms_yaml = os.listdir(os.path.join(return_config_path(), 'platforms'))
        found_a_platform = False
        for supported_platform_yaml in supported_platforms_yaml:
            supported_platform = supported_platform_yaml.split('.')[0]
            if supported_platform in hostname:
                platform = supported_platform
                found_a_platform = True
                break

        if found_a_platform:
            # Set found platform in the dictionary
            internal_config_dict['configure_options']['platform'] = platform

            # Load platform config and set default modules
            platform_path_file = os.path.join(return_config_path(), 'platforms', platform + '.yaml')
            platform_dict = load_yaml(logger, platform_path_file)
            default_modules = platform_dict['modules']['default_modules']
            internal_config_dict['configure_options']['modules'] = default_modules

            # Append build with the modules being used
            build_dir = build_dir + '-' + default_modules

        # Set the list of bundles
        bundles_yaml = os.listdir(os.path.join(return_config_path(), 'bundles'))
        bundles = []
        for bundle_yaml in bundles_yaml:
            if bundle_yaml != 'build-order.yaml':
                bundles.append(bundle_yaml.split('.')[0])
        internal_config_dict['clone_options']['bundles'] = bundles

        # Set the path to the build directory
        cmake_build_type = internal_config_dict['configure_options']['cmake_build_type']
        build_dir = build_dir + '-' + cmake_build_type

        internal_config_dict['configure_options']['path_to_build'] = build_dir

        # Set path to new file and remove if existing
        config_file = os.path.join(os.getcwd(), config_file_name)
        prompt_and_remove_file(logger, config_file)

        # Write dictionary to user directory
        with open(config_file, 'w') as config_file_handle:
            yaml.dump(internal_config_dict, config_file_handle, default_flow_style=False)

        # Tell user to update the file
        logger.info(f'Configuration file generated and written to {config_file}')

        exit(0)

    else:

        if len(tasks_and_config) < 2:
            logger.abort('The number of arguments passed to jedi_bundle must be 0 or >= 2')

        tasks = tasks_and_config[0:-1]
        config_file_name = tasks_and_config[-1]

        # Read the config
        # ---------------
        config_dict = load_yaml(logger, config_file_name)

        # Execute the tasks
        # -----------------

        # Convert to lower case
        tasks = [task.lower() for task in tasks]

        # Check that the options are valid
        valid_tasks = ['clone', 'configure', 'make', 'all']
        for task in tasks:
            if task not in valid_tasks:
                logger.abort(f'Task \'{task}\' not in the valid tasks {valid_tasks}. Ensure the ' +
                             f'configuration is passed as the last argument.')

        # Dictionaries
        clone_dict = config_dict['clone_options']
        configure_dict = {**clone_dict, **config_dict['configure_options']}
        make_dict = {**configure_dict, **config_dict['make_options']}

        # Run the build stages
        if 'all' in tasks or 'clone' in tasks:
            clone_jedi(logger, clone_dict)
        if 'all' in tasks or 'configure' in tasks:
            configure_jedi(logger, configure_dict)
        if 'all' in tasks or 'make' in tasks:
            make_jedi(logger, make_dict)

# --------------------------------------------------------------------------------------------------
