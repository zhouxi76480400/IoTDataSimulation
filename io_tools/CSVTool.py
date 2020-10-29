from io_tools import DiskTool
import os.path
from data_set.private_mobile_device_object import PrivateMobileDeviceObject


def make_a_summary_form(file_name, name_list: list, data_list: list):
    print("Try to make a summary form ...")
    print("\t the file will save to:")
    output_path = os.path.join(DiskTool.create_output_directory(), file_name) + ".csv"
    print("\t\t" + output_path)
    csv = "user id,record counts,timestamp min,timestamp max\n"
    i = 0
    for name in name_list:
        now_data_list = data_list[i]
        timestamp_min = 0
        timestamp_max = 0
        count = len(now_data_list)
        if count > 0:
            timestamp_min = now_data_list[0].timestamp_start
            timestamp_max = now_data_list[0].timestamp_stop
            for now_data_obj in now_data_list:
                now_data_object: PrivateMobileDeviceObject = now_data_obj
                # read min
                if now_data_object.timestamp_start < timestamp_min:
                    timestamp_min = now_data_object.timestamp_start
                # read max
                if now_data_object.timestamp_stop > timestamp_max:
                    timestamp_max = now_data_object.timestamp_stop
        # write to csv
        csv += name + "," + str(count) + "," + str(timestamp_min) + "," + str(timestamp_max) + "\n"
        i += 1

    DiskTool.write_to_disk(output_path, csv)
    # clear
    csv = None
    print("\tWrite successful")
