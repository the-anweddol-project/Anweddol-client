import os


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"


def createFileRecursively(path, is_folder=False):
    try:
        os.makedirs(os.path.dirname(path) if not is_folder else path)

    except FileExistsError:
        pass

    if is_folder:
        return

    with open(path, "w") as fd:
        fd.close()
