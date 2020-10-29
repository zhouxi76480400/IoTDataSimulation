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
