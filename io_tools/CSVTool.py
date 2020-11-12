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


def save_matrix_to_csv(file_name, mat: list):
    print("Try to save a csv for " + file_name)
    print("\t the file will save to:")
    output_path = os.path.join(DiskTool.create_output_directory(), file_name) + ".csv"
    print("\t\t" + output_path)
    csv: str = ""

    for i in range(len(mat)):
        col = ""
        for j in range(len(mat[i])):
            data_value = str(mat[i][j])
            col += data_value
            if j + 1 is not len(mat[i]):
                col += ","
        col += "\n"
        csv += col

    DiskTool.write_to_disk(output_path, csv)
    # clear
    csv = None
    print("\tWrite successful")


def save_to_file_all_x_y_data(filename: str, fin_list: list):

    for i in range(len(fin_list)):
        filename_name_full = filename + "_" + str(i+1)
        print("Try to save a csv for " + filename_name_full)
        print("\t the file will save to:")
        output_save_to_path = os.path.join(DiskTool.create_output_directory(), "data_from_day_" + str(i+1))
        if not os.path.exists(output_save_to_path):
            os.mkdir(output_save_to_path)
        #
        csv_list = []
        for j in range(len(fin_list[0][0])):
            csv_list.append("")
        #
        all_user_list = fin_list[i]
        for j in range(len(all_user_list)):  # users
            a_day_user_x_y_list = all_user_list[j]
            for k in range(len(a_day_user_x_y_list)):
                an_hour_user_xy_list = a_day_user_x_y_list[k]
                csv = csv_list[k]
                csv += str((an_hour_user_xy_list[0]) * 1.) + "," + str((an_hour_user_xy_list[1] * 1.)) + "\n"
                csv_list[k] = csv

        for j in range(len(fin_list[0][0])):
            csv = csv_list[j]
            save_file_name = os.path.join(output_save_to_path, str(j))
            if not os.path.exists(save_file_name):
                os.mkdir(save_file_name)
            save_file_name = os.path.join(save_file_name, str(j) + ".csv")
            DiskTool.write_to_disk(save_file_name, csv)
        csv_list.clear()

    print("\tWrite successful")


def read_som_matrix(file_path: str):
    return_list = []
    print(file_path)

    return return_list
