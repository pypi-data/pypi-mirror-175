#!/usr/bin/env python3
"""
This module contains RESTCONF functions and tasks related to Nornir.

The functions are ordered as followed:
- Single Nornir RESTCONF tasks
- Nornir RESTCONF tasks in regular function
"""

import sys
import json
import requests
from colorama import Fore, Style, init
from nornir.core import Nornir
from nornir.core.task import Task, Result
from nornir_maze.configuration_management.cli import cli_verify_current_software_version_task
from nornir_maze.utils import (
    print_result,
    task_error,
    nr_filter_inventory_from_host_list,
)

init(autoreset=True, strip=False)


#### Single Nornir RESTCONF Tasks ############################################################################


def rc_cisco_get_task(task: Task, yang_data_query: str) -> Result:
    """
    This custom Nornir task executes a RESTCONF GET request to a yang data query and returns a dictionary with
    the whole RESTCONF response as well as some custom formated data for further processing.
    """
    # RESTCONF HTTP URL
    restconf_path = f"/restconf/data/{yang_data_query}"
    url = f"https://{task.host.hostname}:{task.host['restconf_port']}{restconf_path}"

    # RESTCONF HTTP header
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    # RESTCONF HTTP API call
    rc_response = requests.get(  # nosec
        url=url, headers=headers, auth=(task.host.username, task.host.password), verify=False, timeout=120
    )

    # Result dict to return as task result
    result = {
        "url": url,
        "response": rc_response,
        "method": rc_response.request,
        "status_code": rc_response.status_code,
        "elapsed": rc_response.elapsed.total_seconds(),
        "json": rc_response.json(),
    }

    return Result(host=task.host, result=result)


def rc_verify_current_software_version_task(task: Task, verbose=False) -> Result:
    """
    TBD
    """
    # Get the desired version from the Nornir inventory
    desired_version = task.host["software"]["version"]

    # RESTCONF HTTP URL
    rc_path = "/restconf/data/Cisco-IOS-XE-install-oper:install-oper-data/install-location-information"
    url = f"https://{task.host.hostname}:{task.host['restconf_port']}{rc_path}"
    # RESTCONF HTTP header
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    try:
        # RESTCONF HTTP API call
        response = requests.get(  # nosec
            url=url, headers=headers, auth=(task.host.username, task.host.password), verify=False, timeout=120
        )
    except Exception as error:  # pylint: disable=broad-except
        # Define the result as iosxe_c9200 is not implemented yet
        custom_result = f"'{task.name}' -> NornirResponse: <Success: False>\n" f"\n{error}"
        # Return the custom Nornir result as success
        return Result(host=task.host, custom_result=custom_result, failed=True, use_fallback=True)

    # Get the current version from the task result
    current_version = response.json()["Cisco-IOS-XE-install-oper:install-location-information"][0][
        "install-version-state-info"
    ][0]["version"]
    # Slice the variable to have only the fist 8 characters of the version number which should match to
    # the Cisco version naming convention of xx.xx.xx
    current_version = current_version[:8]
    # Write the current version into the Nornir inventory
    task.host["software"]["current_version"] = current_version
    # Prepare needed variables for further processing
    elapsed = response.elapsed.total_seconds()

    # Define the verbose result
    verbose_result = (
        f"'{task.name}' -> RestconfResponse {response} in {elapsed}s\n"
        f"\nURL: {url}\n"
        f"Method: {response.request}\n"
        f"Response: {response}\n"
        f"Current version from JSON payload: {json.dumps(current_version, sort_keys=True, indent=4)}"
    )

    # If the RESTCONF call was successful
    if response.status_code == 200:
        # If the desired version and the current version are the same
        if desired_version in current_version:
            # Define the summary result
            result_summary = (
                f"'{task.name}' -> RestconfResponse {response} in {elapsed}s\n"
                f"-> Desired version {desired_version} match installed version {current_version}"
            )
            # Define the custom_result variable for print_result
            custom_result = verbose_result if verbose else result_summary

            # Return the custom Nornir result as success
            return Result(host=task.host, custom_result=custom_result)

        # Else the desired version and the current version are not the same
        # Define the summary result
        result_summary = (
            f"'{task.name}' -> RestconfResponse {response} in {elapsed}s\n"
            f"-> Desired version {desired_version} don't match installed version {current_version}"
        )
        # Define the custom_result variable for print_result
        custom_result = verbose_result if verbose else result_summary

        # Return the custom Nornir result as failed
        return Result(host=task.host, custom_result=custom_result, failed=True)

    # If the RESTCONF call was not successful -> The task failed and set the use_fallback to True
    return Result(host=task.host, custom_result=verbose_result, failed=True, use_fallback=True)


#### Nornir RESTCONF tasks in regular Function ###############################################################


def rc_verify_current_software_version(nr_obj: Nornir, verbose=False) -> list:
    """
    TBD
    """

    # Get software version with RESTCONF
    rc_task_result = nr_obj.run(
        task=rc_verify_current_software_version_task,
        name="RESTCONF verify current software version",
        verbose=verbose,
        on_failed=True,
    )

    # Print the Nornir rc_verify_current_software_version_task task result
    print_result(rc_task_result, attrs="custom_result")

    # Create a list with all host that failed the RESTCONF call and need to use the CLI fallback task
    fallback_hosts = [host for host in rc_task_result if hasattr(rc_task_result[host], "use_fallback")]

    # If the fallback_hosts list is empty, the CLI fallback is not needed and the failed_hosts list can be
    # returned. The failed host list contains now only host with not matching software version
    if not fallback_hosts:
        failed_hosts = list(rc_task_result.failed_hosts)

        return failed_hosts

    # Re-filter the Nornir inventory on the failed_hosts only
    nr_obj_fallback = nr_filter_inventory_from_host_list(
        nr_obj=nr_obj,
        filter_reason="CLI fallback for the following hosts:",
        host_list=fallback_hosts,
    )

    # Get software version with CLI
    cli_task_result = nr_obj_fallback.run(
        task=cli_verify_current_software_version_task,
        name="CLI verify current software version",
        verbose=verbose,
        on_failed=True,
    )

    # Print the Nornir cli_verify_current_software_version_task task result
    print_result(cli_task_result, attrs="custom_result")

    # If the task overall task result failed -> Print results and exit the script
    for host in cli_task_result:
        if hasattr(cli_task_result[host], "overall_task_failed"):
            print("\n")
            print(task_error(text="RESTCONF and CLI verify current software version", changed=False))
            print("\U0001f4a5 ALERT: RESTCONF AND CLI VERIFY CURRENT SOFTWARE VERSION FAILED! \U0001f4a5")
            print(
                f"\n{Style.BRIGHT}{Fore.RED}-> Analyse the Nornir output for failed task results\n"
                "-> May apply Nornir inventory changes and run the script again\n"
            )
            sys.exit(1)

    # List to fill with all hosts not matching the desired software version
    failed_hosts = list(cli_task_result.failed_hosts) + list(rc_task_result.failed_hosts)

    return failed_hosts
