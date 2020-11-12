from data_tools import DataProcessTool
import numpy as np
import os
from io_tools import CSVTool
from io_tools import DataSetTool
from data_tools import ClusterTool

workspace_path = os.path.join(os.path.split(__file__)[0], "output")

data_set_folders = ["data_from_day_3", "data_from_day_4"]

som_matrix_name = "matrix.csv"

all_values_list = []  # all matrix

devices_type_list = DataSetTool.get_all_users_have_mobile_devices_type()

#  load dataset
for data_set_folder in data_set_folders:
    data_path_of_all_day = os.path.join(workspace_path, data_set_folder)
    all_values_of_a_day = []
    for hour in range(24):
        path_to_som_matrix = os.path.join(os.path.join(data_path_of_all_day, str(hour)), som_matrix_name)
        f_ = open(path_to_som_matrix, "r")
        csv_file = f_.read()
        f_.close()
        csv_split = csv_file.split("\n")
        if csv_split[len(csv_split) - 1] == "":
            csv_split.pop(len(csv_split) - 1)
        this_hour_all_data_list = []  # this hour
        for a_line in csv_split:
            all_values_this_line = a_line.split(",")
            all_values_this_line_list = []
            for a_value in all_values_this_line:
                all_values_this_line_list.append(bool(int(a_value)))
            this_hour_all_data_list.append(all_values_this_line_list)
        all_values_of_a_day.append(this_hour_all_data_list)
    all_values_list.append(all_values_of_a_day)


def is_this_user_in_this_cluster(mat, day: int, hour_: int, cluster_position: int, this_user: int):
    is_this_user_in_this_cluster_inner = False
    all_users_in_this_cluster_inner = ClusterTool.find_all_users_in_this_cluster(mat, day, hour_, cluster_position)
    for user_in_this_cluster in all_users_in_this_cluster_inner:
        if user_in_this_cluster == this_user:
            is_this_user_in_this_cluster_inner = True
            break
    return is_this_user_in_this_cluster_inner




if __name__ == '__main__':

    my_user = 3337
    find_user_device_type = 5  # set type

    select_day = 1
    select_hour = 1

    user_1_s_cluster = ClusterTool.find_user_in_which_cluster(all_values_list, select_day, select_hour, my_user)
    all_users_in_this_cluster = ClusterTool.find_all_users_in_this_cluster(all_values_list, devices_type_list,
                                                                           select_day, select_hour, user_1_s_cluster,
                                                                           device_type=find_user_device_type)
    print(all_users_in_this_cluster)



    # neighbor_clusters = ClusterTool.get_neighbor_clusters(10, 10, 11)
    # for neighbor_cluster in neighbor_clusters:
    #     all_users_in_this_neighbor_cluster = ClusterTool.find_all_users_in_this_cluster(all_values_list, select_day,
    #                                                                                     select_hour, neighbor_cluster)









    # print(all_users_in_this_cluster)





# check user 1 to use


# print(all_values_matrix)









# CSVTool.read_som_matrix()





# DataProcessTool.classification_all_users_from_result_matrix()

# classification_all_users_from_result_matrix