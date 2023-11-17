import os

from dotenv import load_dotenv


def abs_path_resource():
    load_dotenv()
    resource = os.getenv("PATH_RESOURCES")
    path = os.path.abspath(resource)
    return path