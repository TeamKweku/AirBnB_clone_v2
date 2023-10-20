#!/usr/bin/python3
"""distributing an archive to your web servers, using the function do_deploy"""
import os

from fabric.api import *

# import sys

env.hosts = ["34.207.237.135", "54.146.62.81"]
# env.user = 'ubuntu'


def do_deploy(archive_path):
    """function that deploys and archieve to connected web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")

        filename = os.path.basename(archive_path)
        archive_name = filename.split(".")[0]

        path = "/data/web_static/releases/{}".format(archive_name)

        # create the directory
        run("mkdir -p {}".format(path))
        # unarchieve into the stated path
        run("tar -xzf /tmp/{} -C {}".format(filename, path))
        # remove tar file from server
        run("rm /tmp/{}".format(filename))

        run("mv {}/web_static/* {}".format(path, path))
        # Remove the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(path))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
