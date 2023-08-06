import time

import click
from colorama import Fore, Style
from halo import Halo
from github import (BadCredentialsException, Github, GithubException,
                    TwoFactorException)

from sph.workspace import Workspace
from sph.config import configCreate, configSaveToken
from sph.editable import create_editable_from_workspace


@click.command()
@click.option("--github-token", "-gt")
@click.argument("workspace")
def check(github_token, workspace):

    github_client = None;

    config, config_path = configCreate()

    if github_token:
        configSaveToken(config, config_path, github_token)

    github_token = config['github']['access_token']

    try:
        if not github_token:
            github_username = click.prompt('Github username')
            github_password = click.prompt('Github password')
            github_client = Github(github_username, github_password)
        else:
            github_client = Github(github_token)

        user = github_client.get_user()
        Halo(f'Logged in github as {user.login}').succeed()
    except BadCredentialsException as e:
        click.echo('Wrong github credentials')
        click.echo(e)
        raise click.Abort()
    except TwoFactorException as e:
        click.echo(
            'Can\'t use credentials for account with 2FA. Please use an' +
            ' access token.'
        )
        click.echo(e)
        raise click.Abort()
    except GithubException as e:
        click.echo('Github issue')
        click.echo(e)
        raise click.Abort()

    # Get dependency tree
    workspace_data = Workspace(workspace)
    editables = create_editable_from_workspace(workspace_data, github_client)

    click.echo()

    editable_version_by_name = dict()

    for ref, path in workspace_data.editables:
        if ref.name not in editable_version_by_name:
            editable_version_by_name[ref.name] = dict()

        if ref.conan_ref not in editable_version_by_name[ref.name]:
            editable_version_by_name[ref.name][ref.conan_ref] = set()

        editable_version_by_name[ref.name][ref.conan_ref].add("workspace")



    for e in editables:
        for ref in e.required_local_lib:
            if ref.name not in editable_version_by_name:
                editable_version_by_name[ref.name] = dict()

            if ref.conan_ref not in editable_version_by_name[ref.name]:
                editable_version_by_name[ref.name][ref.conan_ref] = set()

            editable_version_by_name[ref.name][ref.conan_ref].add(e.ref.conan_ref)

        for ref in e.required_external_lib:
            if ref.name not in editable_version_by_name:
                editable_version_by_name[ref.name] = dict()

            if ref.conan_ref not in editable_version_by_name[ref.name]:
                editable_version_by_name[ref.name][ref.conan_ref] = set()

            editable_version_by_name[ref.name][ref.conan_ref].add(e.ref.conan_ref)

    for e in editables:
        for req in e.required_local_lib:
            for ref_needed, value in editable_version_by_name[req.name].items():
                if (e.ref.conan_ref not in value) and (ref_needed is not req.conan_ref):
                    req.conflicts.append(value)

        for req in e.required_external_lib:
            for ref_needed, value in editable_version_by_name[req.name].items():
                if (e.ref.conan_ref not in value) and (ref_needed is not req.conan_ref):
                    req.conflicts.append(value)

    for e in editables:
        click.echo(f"{Fore.CYAN}{e.ref.conan_ref}{Fore.RESET} at {Fore.YELLOW}{e.conan_path.parents[1]}{Fore.RESET}")
        if e.repo.is_dirty():
            Halo("Repo is dirty").fail()
        else:
            Halo("Repo is clean").succeed()
            checking_workflow(e)
        if len(e.required_local_lib) + len(e.required_external_lib) == 0:
            Halo("No dependency").succeed()
        for req in e.required_local_lib:
            req.print_check(1)
        for req in e.required_external_lib:
            req.print_check(1)
        click.echo()

    # Create a list of all dependencies and their version
    # Check version of non local dependencies
    # Give list of version for non local dependencies with conflict
    # Check dirtiness of local dependencies
    # Check workflow state of local dependencies

