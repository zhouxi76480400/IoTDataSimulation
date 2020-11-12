import os
from io_tools import DataSetTool


def write_to_disk(path, content):
    if content is not None:
        fd = open(path, "w")
        fd.write(content)
        fd.flush()
        fd.close()


def create_output_directory():
    output_file_path = os.path.join(DataSetTool.get_file_path(DataSetTool.get_file_path(__file__)), "output")
    if not os.path.exists(output_file_path):
        os.mkdir(output_file_path)
    return output_file_path


def get_output_directory_path(py_file: str):
    return_path = ""
    if py_file is not None:
        dir_ = os.path.join(os.path.split(os.path.abspath(py_file))[0], "output")
        return_path = dir_
    return return_path
