#!/usr/bin/python3
""" fabric script that generates a .tgz archieve from the content of the
web_static folder """
from fabric.api import local
from datetime import datetime
import os


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
