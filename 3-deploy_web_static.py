#!/usr/bin/python3
"""create and distribute an archive to your web servers,
using the function do_deploy"""
import os
from datetime import datetime

from fabric.api import *

env.hosts = ["34.207.237.135", "54.146.62.81"]


def do_pack():
    """a function that generates a .tgz archieve"""
    if not os.path.exists("versions"):
        local("mkdir versions")

    now = datetime.now()
    str_date = now.strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(str_date)
    archieve_path = os.path.join("versions", archive_name)

    created = local("tar -cvzf {} web_static".format(archieve_path))

    if created.failed:
        return None
    else:
        return archieve_path


@runs_once
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


def deploy():
    """Deploy the archive to web servers."""
    archive_path = do_pack()

    if archive_path is None:
        return False

    return do_deploy(archive_path)
