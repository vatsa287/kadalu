"""
'storage-remove' sub command
"""

# noqa # pylint: disable=duplicate-code
# noqa # pylint: disable=too-many-branches

#To prevent Py2 to interpreting print(val) as a tuple.
from __future__ import print_function
<<<<<<< HEAD
=======
from string import Template
>>>>>>> aa55e4d34cd91cded58fe1dfbe28eddb42982be3

import os
import tempfile
import sys
import json

import utils
<<<<<<< HEAD
from storage_yaml import to_storage_yaml
=======

YAML_TEMPLATE = """apiVersion: "kadalu-operator.storage/v1alpha1"
kind: "KadaluStorage"
metadata:
  name: "${name}"
"""
>>>>>>> aa55e4d34cd91cded58fe1dfbe28eddb42982be3


def set_args(name, subparsers):
    """ add arguments, and their options """

    parser = subparsers.add_parser(name)
    arg = parser.add_argument

    arg(
        "name",
        help="Storage Name"
    )
    utils.add_global_flags(parser)


def validate(args):
    """
    Validate the storage requested to be deleted
    is present in kadalu configmap or not.
    Exit if not present.
    """

<<<<<<< HEAD
    storage_info_data = get_configmap_data(args.name)
=======
    storage_info_data = get_configmap_data(args)
>>>>>>> aa55e4d34cd91cded58fe1dfbe28eddb42982be3

    if storage_info_data is None:
        print("Aborting.....")
        print("Invalid name. No such storage '%s' in Kadalu configmap." % args.name)
        sys.exit(1)


<<<<<<< HEAD
def get_configmap_data(volname):
=======
def get_configmap_data(args):
>>>>>>> aa55e4d34cd91cded58fe1dfbe28eddb42982be3
    """
    Get storage info data from kadalu configmap
    """

    cmd = utils.kubectl_cmd(args) + ["get", "configmap", "kadalu-info", "-nkadalu", "-ojson"]

    try:
        resp = utils.execute(cmd)
        config_data = json.loads(resp.stdout)

<<<<<<< HEAD
=======
        volname = args.name
>>>>>>> aa55e4d34cd91cded58fe1dfbe28eddb42982be3
        data = config_data['data']
        storage_name = "%s.info" % volname
        storage_info_data = data[storage_name]

        # Return data in 'dict' format
        return json.loads(storage_info_data)

    except utils.CommandError as err:
        utils.command_error(cmd, err.stderr)

    except KeyError:
        # Validate method expects None when 'storage' not found.
        return None


def storage_add_data(args):
    """ Build the config file """

<<<<<<< HEAD
    storage_info_data = get_configmap_data(args.name)

=======
>>>>>>> aa55e4d34cd91cded58fe1dfbe28eddb42982be3
    content = {
        "apiVersion": "kadalu-operator.storage/v1alpha1",
        "kind": "KadaluStorage",
        "metadata": {
            "name": args.name
<<<<<<< HEAD
        },
        "spec": {
            "type": storage_info_data['type'],
            "storage": []
        }
    }

    # External details are specified, no 'storage' section required
    if storage_info_data['type'] == "External":
        # TODO: Check keynames from kadalu configmap and set node, vol
        node = ""
        vol = ""
        content["spec"]["details"] = [
            {
                "gluster_host": node,
                "gluster_volname": vol.strip("/")
            }
        ]
        return content

    # Everything below can be provided for a 'Replica3' setup.
    # Or two types of data can be provided for 'Replica2'.
    # So, return only at the end.

    bricks = storage_info_data.get('bricks')

    for brick in bricks:

        # If Device is specified
        if brick['brick_device']:

            node = brick['node']
            dev = brick['brick_device']
            content["spec"]["storage"].append(
                {
                    "node": node,
                    "device": dev
                }
            )

        # If Path is specified
        if brick['host_brick_path']:

            node = brick['node']
            path = brick['host_brick_path']
            content["spec"]["storage"].append(
                {
                    "node": node,
                    "path": path
                }
            )

        # If PVC is specified
        if brick['pvc_name']:

            pvc = storage_info_data['pvc_name']
            content["spec"]["storage"].append(
                {
                    "pvc": pvc
                }
            )

=======
        }
    }

>>>>>>> aa55e4d34cd91cded58fe1dfbe28eddb42982be3
    return content


def run(args):
    """ Adds the subcommand arguments back to main CLI tool """
<<<<<<< HEAD
    data = storage_add_data(args)

    yaml_content = to_storage_yaml(data)
=======

    yaml_content = Template(YAML_TEMPLATE).substitute(name=args.name)

>>>>>>> aa55e4d34cd91cded58fe1dfbe28eddb42982be3
    print("Storage Yaml file for your reference:\n")
    print(yaml_content)

    if args.dry_run:
        return

    if not args.script_mode:
        answer = ""
        valid_answers = ["yes", "no", "n", "y"]

        while answer not in valid_answers:
            answer = input("Is this correct?(Yes/No): ")
            answer = answer.strip().lower()

        if answer in ["n", "no"]:
            return

    config, tempfile_path = tempfile.mkstemp(prefix="kadalu")
    try:
        with os.fdopen(config, 'w') as tmp:
            tmp.write(yaml_content)

        cmd = utils.kubectl_cmd(args) + ["delete", "-f", tempfile_path]
        resp = utils.execute(cmd)
<<<<<<< HEAD
        print("Storage delete request sent successfully")
=======
        print("Storage delete request sent successfully.\n")
>>>>>>> aa55e4d34cd91cded58fe1dfbe28eddb42982be3
        print(resp.stdout)
        print()

    except utils.CommandError as err:
        os.remove(tempfile_path)
        utils.command_error(cmd, err.stderr)

    except FileNotFoundError:
        os.remove(tempfile_path)
        utils.kubectl_cmd_help(args.kubectl_cmd)

    finally:
        if os.path.exists(tempfile_path):
            os.remove(tempfile_path)
