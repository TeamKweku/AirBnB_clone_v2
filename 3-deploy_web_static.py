#!/usr/bin/python3
"""create and distribute an archive to your web servers,
using the function do_deploy"""
from fabric.api import *
from datetime import datetime
import os


env.hosts = ["18.206.202.36", "100.26.160.231"]


def do_pack():
    """a function that generates a .tgz archieve"""
    if not os.path.exists("versions"):
        local("mkdir versions")

    now = datetime.now()
    str_date = now.strftime("%Y%m%d%H%M%S")
    archive_name = f"web_static_{str_date}.tgz"
    archieve_path = os.path.join("versions", archive_name)

    created = local(f"tar -cvzf {archieve_path} web_static")

    if created.failed:
        return None
    else:
        return archieve_path


def do_deploy(archive_path):
    """function that deploys and archieve to connected web servers"""
    if not os.path.exists(archive_path):
        return False

    try:
        put(archive_path, "/tmp/")

        filename = os.path.basename(archive_path)
        archive_name = filename.split(".")[0]

        path = f"/data/web_static/releases/{archive_name}"

        # create the directory
        run(f"mkdir -p {path}")
        # unarchieve into the stated path
        run(f"tar -xzf /tmp/{filename} -C {path}")
        # remove tar file from server
        run(f"rm /tmp/{filename}")

        run(f"mv {path}/web_static/* {path}")
        # Remove the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run(f"ln -s {path} /data/web_static/current")

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
