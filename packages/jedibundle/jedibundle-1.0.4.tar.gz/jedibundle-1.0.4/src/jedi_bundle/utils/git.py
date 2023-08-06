#!/usr/bin/env python

# (C) Copyright 2022 United States Government as represented by the Administrator of the
# National Aeronautics and Space Administration. All Rights Reserved.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.

# --------------------------------------------------------------------------------------------------


import os
import requests
import subprocess

from jedi_bundle.utils.config import config_get
from jedi_bundle.utils.file_system import devnull, subprocess_run


# --------------------------------------------------------------------------------------------------


def get_github_username_token(logger):

    # Extract github username from /home/user/git-credentials
    user = os.getenv('USER')
    git_cred_path = os.path.join('/home', user, '.git-credentials')
    try:
        with open(git_cred_path) as f:
            git_cred_line = f.readlines()[0].rstrip()
        git_cred_line = git_cred_line.replace('https://', '')
        git_cred_line = git_cred_line.replace('@github.com', '')
        username, token = git_cred_line.split(':')
    except Exception as e:
        logger.info(f'Credentials {git_cred_path} not found. Private repos wont be found.')
        username = ''
        token = ''

    return username, token


# --------------------------------------------------------------------------------------------------


def repo_is_reachable(logger, url, username, token):

    # Default is that the repo is not reachable
    is_reachable = False

    try:
        get = requests.get(url, auth=(username, token))
        if get.status_code == 200:
            # Check that the full name provided by API is expected path.
            # Sometimes this value is inconsistent with the repo path.
            gh_api_dict = get.json()
            if 'full_name' in gh_api_dict:
                full_name = gh_api_dict['full_name']
                if full_name in url:
                    is_reachable = True
    except Exception:
        is_reachable = False

    return is_reachable


# --------------------------------------------------------------------------------------------------


def repo_has_branch(logger, url, branch, is_tag=False):

    # Command to check if branch exists and pass exit code back
    heads_or_tags = '--heads'
    if is_tag:
        heads_or_tags = '--tags'

    git_ls_cmd = ['git', 'ls-remote', heads_or_tags, '--exit-code', url, branch]

    # Run command
    process = subprocess.run(git_ls_cmd, stdout=devnull)

    # Return flag based on exit code.
    if process.returncode == 0:
        return True
    else:
        return False


# --------------------------------------------------------------------------------------------------


def get_url_and_branch(logger, github_orgs, repo_url_name, default_branch, user_branch, is_tag_in):

    # Get GitHub username and token if .git-credentials file available
    username, token = get_github_username_token(logger)

    # Track finding of the user branch and the default branch
    found_default_branch = False

    # Loop over URLs
    repo_url_found = False
    repo_url_to_use = ''
    repo_branch_to_use = ''
    for github_org in github_orgs:

        # Full path of the repo url
        github_url = os.path.join('https://github.com', github_org, repo_url_name)
        github_api_url = os.path.join('https://api.github.com/repos', github_org, repo_url_name)

        # Check it the repo url is reachable
        if repo_is_reachable(logger, github_api_url, username, token):

            # Assert that the repo was found somewhere
            repo_url_found = True

            # Check for user branch and return right away if found
            if user_branch != '':
                if repo_has_branch(logger, github_url, user_branch):
                    is_tag = False
                    return repo_url_found, github_url, user_branch, is_tag

            # Track first instance of finding the default branch. But do not exit when it's first
            # found so that other organizations can be checked for the user branch.
            if not found_default_branch:
                if repo_has_branch(logger, github_url, default_branch, is_tag_in):
                    found_default_branch = True
                    repo_url_found = True
                    repo_url_to_use = github_url
                    repo_branch_to_use = default_branch
                    is_tag = is_tag_in

    return repo_url_found, repo_url_to_use, repo_branch_to_use, is_tag


# --------------------------------------------------------------------------------------------------


def clone_git_repo(logger, url, branch, target, is_tag):

    # Check if directory already exists
    if not os.path.exists(target):

        # Command to check if branch exists and pass exit code back
        git_clone_cmd = ['git', 'clone', '--recursive', '-b', branch, url, target]

        # Run command
        subprocess_run(logger, git_clone_cmd, True)

    elif is_tag:

        logger.info(f'Repo {url}, tag already cloned, skipping...')

    else:

        # Write info
        logger.info(f'Repo {url}, already cloned. Updating branch...')

        # Switch to directory where repo is cloned
        cwd = os.getcwd()
        os.chdir(target)

        # Fetch
        cmd = ['git', 'fetch']
        subprocess_run(logger, cmd, True)

        # Switch to branch
        cmd = ['git', 'checkout', branch]
        subprocess_run(logger, cmd, True)

        # Pull latest
        cmd = ['git', 'pull', 'origin', branch]
        subprocess_run(logger, cmd, True)

        # Switch back to other directory
        os.chdir(cwd)


# --------------------------------------------------------------------------------------------------
