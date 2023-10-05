#!/usr/bin/python3
"""distributing an archive to your web servers, using the function do_deploy"""
from fabric.api import *
import os
# import sys

env.hosts = ['18.206.202.36', '100.26.160.231']
# env.user = 'ubuntu'


def do_deploy(archive_path):
    """function that deploys and archieve to connected web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")

        filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(filename)[0]

        path = f"/data/web_static/releases/{archive_name}"

        # create the directory
        run(f"mkdir -p {path}")
        # unarchieve into the stated path
        run(f"tar -xzf /tmp/{filename} -C {path}")
        # remove tar file from server
        run(f"rm /tmp/{filename}")
        # Remove the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run(f"ln -s {path} /data/web_static/current")

        print("New version deployed!")
        return True

    except Exception as e:
        return False
