import os
import tests


def path_dir(*file_path):
    return os.path.abspath(os.path.join(os.path.dirname(tests.__file__), *file_path))
