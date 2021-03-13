"""
'logs' subcommand for kubectl-kadalu CLI tool
"""
# To prevent Py2 to interpreting print(val) as a tuple.
from __future__ import print_function

import sys
import argparse
import utils


# TODO: provide 'hint' based on grepping error logs. That way, users get to
#       check for few common errors easily

def set_args(name, subparsers):
    """ add arguments to argparser """
    # TODO: provide options to pass options to kubectl logs (like tail, container name etc)

    parser = subparsers.add_parser(
        name,
        formatter_class=argparse.RawTextHelpFormatter
    )

    arg = parser.add_argument

    arg("-p", "--podname",
        help="Specify pod name to get log info")

    arg("-c", "--container",
        help="Specify container name to get log info.\n"
             "To be used along with '--podname'")

    arg("-A", "--allcontainers", action="store_true",
        help=("Show logs of all containers"
              "of a particular pod.\n"
              "To be used along with '--podname'"))

    utils.add_global_flags(parser)


def validate(args):
    """Validate optional arguments"""

    if args.container and not args.podname:
        print("Specify pod name for the container '%s'." %args.container)
        sys.exit(1)

    if args.allcontainers and not args.podname:
        print("Specify pod name for displaying of all containers.\n"
              "Use without any optional arguments to get logs of "
              "all pods and all of it's containers.")
        sys.exit(1)

    if args.allcontainers and args.container:
        print("Cannot use both --allcontainers & --container together. "
              "Choose any one of the above options.")
        sys.exit(1)


def fetch_pod_logs(args):
    """ Get logs for a particular pod """
    try:
        # Set default to '--allcontainers' to avoid exception
        container_name = ""
        if args.allcontainers:
            container_name = "--all-containers"
        elif args.container:
            container_name = args.container

        log_cmd = utils.kubectl_cmd(args) + [
            "logs", "-nkadalu",
            args.podname, container_name]
        log_resp = utils.execute(log_cmd)
        print("----- (Kadalu Namespace) %s -----" % args.podname)
        print(log_resp.stdout)
        print()

    except FileNotFoundError:
        utils.kubectl_cmd_help(args.kubectl_cmd)
    except utils.CommandError as err:
        utils.command_error(log_cmd, err.stderr)

def run(args):
    """ perform log subcommand """

    try:
        if args.podname:
            fetch_pod_logs(args)
        else:
            cmd = utils.kubectl_cmd(args) + ["get", "pods", "-nkadalu", "-oname"]
            resp = utils.execute(cmd)
            pods = resp.stdout.split('\n')

            for pod in pods:
                if pod == "":
                    continue
                log_cmd = utils.kubectl_cmd(args) + [
                    "logs", "-nkadalu",
                    pod, "--all-containers=true"]
                log_resp = utils.execute(log_cmd)
                print("----- (Kadalu Namespace) %s -----" % pod)
                print(log_resp.stdout)
                print()

    except utils.CommandError as err:
        utils.command_error(cmd, err.stderr)
    except FileNotFoundError:
        utils.kubectl_cmd_help(args.kubectl_cmd)
