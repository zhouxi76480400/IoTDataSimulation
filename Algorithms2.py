from data_tools import DataProcessTool
import numpy as np
import os
from io_tools import CSVTool
from io_tools import DataSetTool
from data_tools import ClusterTool
import math
import random

workspace_path = os.path.join(os.path.split(__file__)[0], "output")

chart_data_save_path = os.path.join(workspace_path, "chart_data")

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


all_uses_xy_dict = {}


def read_all_user_s_x_y_list(day: int, hour_: int):
    all_xy = []
    file_path = os.path.join(os.path.join(os.path.join(workspace_path, data_set_folders[day - 1]), str(hour_)),
                             str(hour_) + ".csv")

    v_ = all_uses_xy_dict.get(file_path)
    if v_ is not None:
        all_xy = v_
    else:
        csv_x_y = ""
        f = open(file_path, "r")
        csv_x_y = f.read()
        f.close()
        lines = csv_x_y.split("\n")
        if lines[len(lines) - 1] == "":
            lines.pop(len(lines) - 1)

        for now_ in range(len(lines)):
            list_xy = lines[now_].split(",")
            all_xy.append((float(list_xy[0]), float(list_xy[1])))
        all_uses_xy_dict[file_path] = all_xy

    return all_xy


def get_a_user_s_xy(day: int, hour_: int, user_a_name: str):
    all_xy_list = read_all_user_s_x_y_list(day, hour_)
    x, y = all_xy_list[int(user_a_name)]
    return x, y


def calculate_the_user_s_between(day: int, hour_: int, user_a_name: str, user_b_name: str):
    # x
    user_a_x, user_a_y = get_a_user_s_xy(day, hour_, user_a_name)
    #
    user_b_x, user_b_y = get_a_user_s_xy(day, hour_, user_b_name)
    distance = \
        math.sqrt(math.pow(user_b_x - user_a_x, 2) + math.pow(user_b_y - user_a_y, 2))
    return distance


def has_this_type_device(user_name: str, device_type: int):
    has: bool = devices_type_list[int(user_name)][device_type - 1]
    return has


def find_close_users(day: int, hour_: int, my_user_name: str, range_: float, interest_device_type: int):
    traffic_count = 0
    distance_list = []
    for user_tmp in range(4000):
        user_tmp_name = str(user_tmp)
        between_ = calculate_the_user_s_between(day, hour_, my_user_name, user_tmp_name)
        if between_ <= range_:
            # check is not my self
            if user_tmp_name != my_user_name:
                # check is interest
                traffic_count += 1
                if has_this_type_device(user_tmp_name, interest_device_type):
                    distance_list.append((user_tmp_name, between_))
    return distance_list, traffic_count


def sort_get_distance(close_user):
    return close_user[1]


def algorithm2(day: int, hour_: int, my_user_name: str, interest_device_type: int, range_expand_each_time: float):
    traffic_counter = 0
    range_ = range_expand_each_time
    max_try_times = int(1. / range_expand_each_time)
    #
    close_users = []
    while len(close_users) < 1 and traffic_counter < max_try_times:
        close_users, f_counter = find_close_users(day, hour_, my_user_name, range_, interest_device_type)
        traffic_counter += 1
        range_ += range_expand_each_time
    close_users = sorted(close_users, key=sort_get_distance)

    # print("bbbb:" + str(close_users))

    return traffic_counter, close_users[0][1]  # range_


def check_cluster_check_left_time(found_list):
    left_time = 0
    for bool_i in found_list:
        if not bool_i:
            left_time += 1
    return left_time


def get_not_checked_clusters(found_list, neighbor_list):
    not_checked_list = []
    for neighbor in neighbor_list:
        if not found_list[neighbor]:
            not_checked_list.append(neighbor)
    return not_checked_list


def get_neighbor_clusters_not_search(now_cluster, cluster_found_list):
    ret_ = []
    neighbors = ClusterTool.get_neighbor_clusters(10, 10, now_cluster)
    for neighbor in neighbors:
        if not cluster_found_list[neighbor]:
            ret_.append(neighbor)
    return ret_


def add_into_hit_list(hit_list, found_list):
    for fff_ in found_list:
        hit_list[fff_] = True


def print_hit_list(hit_list):
    lllla = []
    i = 0
    for wwwwW in hit_list:
        if wwwwW:
            lllla.append(i)
        i += 1


def get_all_neighbor_s_neighbor(hit_list, all_neighbor):
    all_nb_nb = []
    for nb in all_neighbor:
        nb_nb = ClusterTool.get_neighbor_clusters(10, 10, nb)
        for nb_nb_nb in nb_nb:
            if not hit_list[nb_nb_nb]:
                all_nb_nb.append(nb_nb_nb)
    #
    all_nb_nb = list(set(all_nb_nb))
    return all_nb_nb


def algorithm1_sub1(hit_list, neighbors):
    add_into_hit_list(hit_list, neighbors)
    return get_all_neighbor_s_neighbor(hit_list, neighbors)


def algorithm1(day: int, hour_: int, my_user_name: str, interest_device_type: int):
    traffic = 1
    #
    hit_list = []
    for h_pos in range(100):
        hit_list.append(False)

    #
    first_cluster = ClusterTool.find_user_in_which_cluster(all_values_list, day, hour_, int(my_user_name))
    neighbors = [first_cluster]

    hit_list[first_cluster] = True
    #
    neighbor_users = ClusterTool.find_all_users_in_this_cluster(all_values_list, devices_type_list, day, hour_,
                                                                first_cluster, interest_device_type)
    if len(neighbor_users) == 1:
        if str(neighbor_users[0]) == my_user_name:
            neighbor_users = []

    if len(neighbor_users) == 0:
        while check_cluster_check_left_time(hit_list) > 0 and not len(neighbor_users) > 0:
            neighbors = algorithm1_sub1(hit_list, neighbors)
            # print(neighbors)
            for neighbor in neighbors:
                neighbor_users = \
                    ClusterTool. \
                        find_all_users_in_this_cluster(all_values_list,
                                                       devices_type_list,
                                                       day, hour_, neighbor, interest_device_type)
                traffic += 1
                if len(neighbor_users) > 0:
                    break
    range_list = []
    # print("aaaa:" + str(neighbor_users))
    if len(neighbor_users) > 0:
        for neighbor_user in neighbor_users:
            if str(neighbor_user) != my_user_name:
                range_list.append(calculate_the_user_s_between(day, hour_, str(my_user_name), str(neighbor_user))
                              )
        if len(range_list) == 0:
            print("用0")
            return traffic, 0
        else:
            return traffic, min(range_list)
    return traffic, -1


def save_list_to_csv(list_, save_file_path):
    csv_a = ""
    for ele in list_:
        csv_a += str(ele) + "\n"
    fi = open(save_file_path, "w")
    fi.write(csv_a)
    fi.close()
    csv_a = None


def a1(day: int, hour_: int, my_user_name: str, interest_device_type: int):
    traffic = 1
    #
    hit_list = []
    for h_pos in range(100):
        hit_list.append(False)
    #
    first_cluster = ClusterTool.find_user_in_which_cluster(all_values_list, day, hour_, int(my_user_name))
    neighbors = [first_cluster]

    hit_list[first_cluster] = True
    #
    neighbor_users = ClusterTool.find_all_users_in_this_cluster(all_values_list, devices_type_list, day, hour_,
                                                                first_cluster, interest_device_type)
    if len(neighbor_users) == 1:
        if str(neighbor_users[0]) == my_user_name:
            neighbor_users = []

    if len(neighbor_users) == 0:
        while check_cluster_check_left_time(hit_list) > 0 and not len(neighbor_users) > 0:
            neighbors = algorithm1_sub1(hit_list, neighbors)
            # print(neighbors)
            for neighbor in neighbors:
                neighbor_users = \
                    ClusterTool. \
                        find_all_users_in_this_cluster(all_values_list,
                                                       devices_type_list,
                                                       day, hour_, neighbor, interest_device_type)
                traffic += 1
                if len(neighbor_users) > 0:
                    break
    range_list = []
    # print("aaaa:" + str(neighbor_users))
    if len(neighbor_users) > 0:
        for neighbor_user in neighbor_users:
            if str(neighbor_user) != my_user_name:
                range_list.append(calculate_the_user_s_between(day, hour_, str(my_user_name), str(neighbor_user))
                              )
        if len(range_list) == 0:
            print("用0")
            return traffic, 0
        else:
            return traffic, min(range_list)
    return traffic, -1


def a2(day: int, hour_: int, my_user_name: str, interest_device_type: int, range_expand_each_time: float):
    traffic_counter = 0
    range_ = range_expand_each_time
    max_try_times = int(math.sqrt(2) / range_expand_each_time) + 1
    #
    close_users = []
    while len(close_users) < 1 and traffic_counter < max_try_times:
        close_users, traffic_counter_now = find_close_users(day, hour_, my_user_name, range_, interest_device_type)
        traffic_counter += traffic_counter_now
        range_ += range_expand_each_time
    close_users = sorted(close_users, key=sort_get_distance)

    nearest = math.sqrt(2)
    if len(close_users) != 0:
        nearest = close_users[0][1]

    return traffic_counter, nearest  # range_


#################################################################################

# x: no. user y: traffic, distance
# def test_the_number_of_users_and_traffic(day_: int, hour_: int):
    # user_count = 100
    #
    # data_list_a_traffic = []
    # data_list_a_traffic_avg = []
    # data_list_a_range = []
    # data_list_a_range_avg = []
    # #
    # data_list_b_traffic = []
    # data_list_b_traffic_avg = []
    # data_list_b_range = []
    # data_list_b_range_avg = []
    #
    # #
    # data_list_kind_of_devices_distance_a = [0, 0, 0, 0, 0]
    # data_list_kind_of_devices_distance_a_max = [0, 0, 0, 0, 0]
    # data_list_kind_of_devices_distance_a_min = [0, 0, 0, 0, 0]
    # data_list_kind_of_devices_distance_b = [0, 0, 0, 0, 0]
    # data_list_kind_of_devices_distance_b_max = [0, 0, 0, 0, 0]
    # data_list_kind_of_devices_distance_b_min = [0, 0, 0, 0, 0]
    # #
    # data_list_kind_of_devices_traffic_a = [0, 0, 0, 0, 0]
    # data_list_kind_of_devices_traffic_a_min = [0, 0, 0, 0, 0]
    # data_list_kind_of_devices_traffic_a_max = [0, 0, 0, 0, 0]
    #
    # data_list_kind_of_devices_traffic_b = [0, 0, 0, 0, 0]
    # data_list_kind_of_devices_traffic_b_min = [0, 0, 0, 0, 0]
    # data_list_kind_of_devices_traffic_b_max = [0, 0, 0, 0, 0]
    #
    # data_list_kind_of_devices = [0, 0, 0, 0, 0]
    #
    # #
    # counter_a_traffic = 0
    # counter_b_traffic = 0
    #
    # #
    # counter_a_range = 0
    # counter_b_range = 0
    #
    # now_day = day_
    # now_time = hour_
    #
    # # for users in range(user_count):
    # for users in range(user_count):
    #     print("number of users:" + str(users))
    #     my_user = str(random.randint(0, user_count - 1))
    #     device_type = random.randint(1, 5)
    #
    #     #
    #     kind_of_device_now = data_list_kind_of_devices[device_type-1]
    #     kind_of_device_now += 1
    #     data_list_kind_of_devices[device_type - 1] = kind_of_device_now
    #
    #     # algorithm1
    #     traffic_counter1, range_1 = algorithm1(now_day, now_time, my_user, device_type)
    #     # algorithm2
    #     traffic_counter2, range_2 = algorithm2(now_day, now_time, my_user, device_type, 0.004)
    #     #
    #     counter_a_traffic += traffic_counter1
    #     counter_b_traffic += traffic_counter2
    #     #
    #     avg_a_traffic = counter_a_traffic / (users + 1)
    #     avg_b_traffic = counter_b_traffic / (users + 1)
    #     #
    #     counter_a_range += range_1
    #     counter_b_range += range_2
    #     avg_a_range = counter_a_range / (users + 1)
    #     avg_b_range = counter_b_range / (users + 1)
    #     #
    #     data_list_a_traffic.append(counter_a_traffic)
    #     data_list_a_traffic_avg.append(avg_a_traffic)
    #     data_list_a_range.append(counter_a_range)
    #     data_list_a_range_avg.append(avg_a_range)
    #     #
    #     data_list_b_traffic.append(counter_b_traffic)
    #     data_list_b_traffic_avg.append(avg_b_traffic)
    #     data_list_b_range.append(counter_b_range)
    #     data_list_b_range_avg.append(avg_b_range)
    #     #
    #
    #     # add type
    #     new_device_type = data_list_kind_of_devices_traffic_a[device_type - 1]
    #     new_device_type += counter_a_traffic
    #     data_list_kind_of_devices_traffic_a[device_type - 1] = new_device_type
    #     #
    #     new_device_type = data_list_kind_of_devices_traffic_b[device_type - 1]
    #     new_device_type += counter_b_traffic
    #     data_list_kind_of_devices_traffic_b[device_type - 1] = new_device_type
    #
    #     # add range
    #     new_distance = data_list_kind_of_devices_distance_a[device_type - 1]
    #     new_distance += counter_a_range
    #     data_list_kind_of_devices_distance_a[device_type - 1] = new_distance
    #
    #     # max
    #     new_max_distance = data_list_kind_of_devices_distance_a_max[device_type - 1]
    #     if new_max_distance == 0:
    #         new_max_distance = range_1
    #     else:
    #         if new_max_distance < range_1:
    #             new_max_distance = range_1
    #     data_list_kind_of_devices_distance_a_max[device_type - 1] = new_max_distance
    #
    #     new_max_distance = data_list_kind_of_devices_distance_b_max[device_type - 1]
    #     if new_max_distance == 0:
    #         new_max_distance = range_2
    #     else:
    #         if new_max_distance < range_2:
    #             new_max_distance = range_2
    #     data_list_kind_of_devices_distance_b_max[device_type - 1] = new_max_distance
    #
    #     # max traffic
    #     new_max_traffic = data_list_kind_of_devices_traffic_a_max[device_type - 1]
    #     if new_max_traffic == 0:
    #         new_max_traffic = traffic_counter1
    #     else:
    #         if new_max_traffic < traffic_counter1:
    #             new_max_traffic = traffic_counter1
    #     data_list_kind_of_devices_traffic_a_max[device_type - 1] = new_max_traffic
    #
    #     new_max_traffic = data_list_kind_of_devices_traffic_b_max[device_type - 1]
    #     if new_max_traffic == 0:
    #         new_max_traffic = traffic_counter2
    #     else:
    #         if new_max_traffic < traffic_counter2:
    #             new_max_traffic = traffic_counter2
    #     data_list_kind_of_devices_traffic_b_max[device_type - 1] = new_max_traffic
    #
    #
    #     # min
    #     new_min_distance = data_list_kind_of_devices_distance_a_min[device_type - 1]
    #     if new_min_distance == 0:
    #         new_min_distance = range_1
    #     else:
    #         if new_min_distance > range_1:
    #             new_min_distance = range_1
    #     data_list_kind_of_devices_distance_a_min[device_type - 1] = new_min_distance
    #
    #     new_min_distance = data_list_kind_of_devices_distance_b_min[device_type - 1]
    #     if new_min_distance == 0:
    #         new_min_distance = range_2
    #     else:
    #         if new_min_distance > range_2:
    #             new_min_distance = range_2
    #     data_list_kind_of_devices_distance_b_min[device_type - 1] = new_min_distance
    #
    #     new_min_traffic = data_list_kind_of_devices_traffic_a_min[device_type - 1]
    #     if new_min_traffic == 0:
    #         new_min_traffic = traffic_counter1
    #     else:
    #         if new_min_traffic > traffic_counter1:
    #             new_min_traffic = traffic_counter1
    #     data_list_kind_of_devices_traffic_a_min[device_type - 1] = new_min_traffic
    #
    #     new_min_traffic = data_list_kind_of_devices_traffic_b_min[device_type - 1]
    #     if new_min_traffic == 0:
    #         new_min_traffic = traffic_counter2
    #     else:
    #         if new_min_traffic > traffic_counter2:
    #             new_min_traffic = traffic_counter2
    #     data_list_kind_of_devices_traffic_b_min[device_type - 1] = new_min_traffic
    #
    #
    #
    #     new_distance = data_list_kind_of_devices_distance_b[device_type - 1]
    #     new_distance += counter_b_range
    #     data_list_kind_of_devices_distance_b[device_type - 1] = new_distance
    #
    #
    #     # print("\t'" + str(avg_a_traffic))
    #     # print("\t'" + str(avg_b_traffic))
    #     # print("\t and")
    #     # print("\t'" + str(counter_a_range))
    #     # print("\t'" + str(counter_b_range))
    #
    # # print(data_list_a_traffic_avg)
    # # print(data_list_b_traffic_avg)
    # # print(data_list_kind_of_devices_traffic_a)
    # # print(data_list_kind_of_devices_traffic_b)
    #
    # print(data_list_kind_of_devices_distance_a_max)
    # print(data_list_kind_of_devices_distance_a_min)
    #
    # # save to
    # if not os.path.isdir(chart_data_save_path):
    #     os.mkdir(chart_data_save_path)
    #
    # # common
    # save_list_to_csv(data_list_kind_of_devices, os.path.join(chart_data_save_path, "common_kind_of_devices.csv"))
    # save_list_to_csv(data_list_a_traffic, os.path.join(chart_data_save_path, "common_a_traffic.csv"))
    # save_list_to_csv(data_list_b_traffic, os.path.join(chart_data_save_path, "common_b_traffic.csv"))
    # save_list_to_csv(data_list_a_range, os.path.join(chart_data_save_path, "common_a_distance.csv"))
    # save_list_to_csv(data_list_b_range, os.path.join(chart_data_save_path, "common_b_distance.csv"))
    #
    # # chart1
    # save_list_to_csv(data_list_a_traffic_avg, os.path.join(chart_data_save_path, "x_users_y_traffic_avg_1.csv"))
    # save_list_to_csv(data_list_b_traffic_avg, os.path.join(chart_data_save_path, "x_users_y_traffic_avg_2.csv"))
    # # chart2
    #
    # for c___ in range(len(data_list_kind_of_devices_traffic_a)):
    #     a_data_list_kind_of_devices_traffic_a = data_list_kind_of_devices_traffic_a[c___]
    #     a_data_list_kind_of_devices = data_list_kind_of_devices[c___]
    #     a_data_list_kind_of_devices_traffic_a_avg = a_data_list_kind_of_devices_traffic_a / a_data_list_kind_of_devices
    #     data_list_kind_of_devices_traffic_a[c___] = a_data_list_kind_of_devices_traffic_a_avg
    #
    #     a_data_list_kind_of_devices_traffic_b = data_list_kind_of_devices_traffic_b[c___]
    #     a_data_list_kind_of_devices_traffic_b_avg = a_data_list_kind_of_devices_traffic_b / a_data_list_kind_of_devices
    #     data_list_kind_of_devices_traffic_b[c___] = a_data_list_kind_of_devices_traffic_b_avg
    #
    #
    #
    #
    # save_list_to_csv(data_list_kind_of_devices_traffic_a, os.path.join(chart_data_save_path, "x_kind_of_devices_y_traffic_avg_1.csv"))
    # save_list_to_csv(data_list_kind_of_devices_traffic_b, os.path.join(chart_data_save_path, "x_kind_of_devices_y_traffic_avg_2.csv"))
    # save_list_to_csv(data_list_kind_of_devices_traffic_a_max, os.path.join(chart_data_save_path, "x_kind_of_devices_y_traffic_max_1.csv"))
    # save_list_to_csv(data_list_kind_of_devices_traffic_a_min, os.path.join(chart_data_save_path, "x_kind_of_devices_y_traffic_min_1.csv"))
    # # save_list_to_csv(data_list_kind_of_devices_traffic_b, os.path.join(chart_data_save_path, "x_kind_of_devices_y_traffic_sum_2.csv"))
    # save_list_to_csv(data_list_kind_of_devices_traffic_b_max, os.path.join(chart_data_save_path, "x_kind_of_devices_y_traffic_max_2.csv"))
    # save_list_to_csv(data_list_kind_of_devices_traffic_b_min, os.path.join(chart_data_save_path, "x_kind_of_devices_y_traffic_min_2.csv"))
    #
    # # chart5
    # save_list_to_csv(data_list_a_range_avg, os.path.join(chart_data_save_path, "x_users_y_distance_avg_1.csv"))
    # save_list_to_csv(data_list_b_range_avg, os.path.join(chart_data_save_path, "x_users_y_distance_avg_2.csv"))
    # # chart6
    # save_list_to_csv(data_list_kind_of_devices_distance_a_max,
    #                  os.path.join(chart_data_save_path, "x_kind_of_devices_y_distance_max_1.csv"))
    # save_list_to_csv(data_list_kind_of_devices_distance_a_min,
    #                  os.path.join(chart_data_save_path, "x_kind_of_devices_y_distance_min_1.csv"))
    # save_list_to_csv(data_list_kind_of_devices_distance_b_max,
    #                  os.path.join(chart_data_save_path, "x_kind_of_devices_y_distance_max_2.csv"))
    # save_list_to_csv(data_list_kind_of_devices_distance_b_min,
    #                  os.path.join(chart_data_save_path, "x_kind_of_devices_y_distance_min_2.csv"))
    # # save_list_to_csv(data_list_kind_of_devices_distance_a, os.path.join(chart_data_save_path, "x_kind_of_devices_y_distance_sum_1.csv"))
    # # save_list_to_csv(data_list_kind_of_devices_distance_b, os.path.join(chart_data_save_path, "x_kind_of_devices_y_distance_sum_2.csv"))



def get_users_by_random_10_percent(all_users_count):
    ret_ = random.sample(range(1, all_users_count), int(all_users_count / 10))
    return ret_


# 1 - 5
def get_interested_device_type():
    device_type = random.randint(1, 5)
    return device_type


def set_max(list_max_or_min, now_type, now_value):
    distance_max_2 = list_max_or_min[now_type - 1]
    if distance_max_2 == 0:
        distance_max_2 = now_value
    else:
        if distance_max_2 < now_value:
            distance_max_2 = now_value
    list_max_or_min[now_type - 1] = distance_max_2


def set_min(list_max_or_min, now_type, now_value):
    distance_max_2 = list_max_or_min[now_type - 1]
    if distance_max_2 == 0:
        distance_max_2 = now_value
    else:
        if distance_max_2 > now_value:
            distance_max_2 = now_value
    list_max_or_min[now_type - 1] = distance_max_2


def set_avg(list_distance_count, list_device_type_count, distance_avg):
    for now_a in range(len(list_distance_count)):
        count_a = list_distance_count[now_a]
        value_a = list_device_type_count[now_a]
        if value_a != 0:
            avg_a = count_a / value_a
        else:
            avg_a = 0
        distance_avg[now_a] = avg_a


def sum_add(list_local, list_global):
    for i_ in range(len(list_local)):
        list_global[i_] += list_local[i_]


def set_max_to_global(list_local, list_global):
    for i_ in range(len(list_global)):
        val_local = list_local[i_]
        list_list_global: list = list_global[i_]
        list_list_global.append(val_local)


def get_all_max_global(list_global):
    list_ret = []
    for a_list in list_global:
        list_ret.append(max(a_list))
    return list_ret


def get_all_min_global(list_global):
    list_ret = []
    for a_list in list_global:
        list_ret.append(min(a_list))
    return list_ret



def get_chart_1_data(day, hour_):
    #
    x_axis = []

    y_axis_traffic_avg_1 = []
    y_axis_traffic_avg_2 = []

    y_axis_distance_avg_1 = []
    y_axis_distance_avg_2 = []

    all_device_type_count = [0, 0, 0, 0, 0]

    y_axis_device_type_and_traffic_max_1 = [[], [], [], [], []]
    # y_axis_device_type_and_traffic_avg_1 = [0, 0, 0, 0, 0]
    y_axis_device_type_and_traffic_min_1 = [[], [], [], [], []]

    y_axis_device_type_and_traffic_max_2 = [[], [], [], [], []]
    # y_axis_device_type_and_traffic_avg_2 = [0, 0, 0, 0, 0]
    y_axis_device_type_and_traffic_min_2 = [[], [], [], [], []]

    y_axis_device_type_and_distance_max_1 = [[], [], [], [], []]
    # y_axis_device_type_and_traffic_avg_1 = [0, 0, 0, 0, 0]
    y_axis_device_type_and_distance_min_1 = [[], [], [], [], []]

    y_axis_device_type_and_distance_max_2 = [[], [], [], [], []]
    # y_axis_device_type_and_traffic_avg_2 = [0, 0, 0, 0, 0]
    y_axis_device_type_and_distance_min_2 = [[], [], [], [], []]


    start_user_count = 100
    max_user_count = 103

    for i in range(start_user_count, max_user_count):
        print("time:" + str(i))
        x_axis.append(i)
        # 隨機個用戶
        all_test_user = get_users_by_random_10_percent(i)
        all_test_user_count = len(all_test_user)
        #
        a_time_traffics_by_1 = []
        a_time_distance_by_1 = []
        a_time_traffics_by_2 = []
        a_time_distance_by_2 = []

        a_time_device_type_count = [0, 0, 0, 0, 0]

        a_time_device_distance_max_1 = [0, 0, 0, 0, 0]
        a_time_device_distance_count_1 = [0, 0, 0, 0, 0]
        a_time_device_distance_min_1 = [0, 0, 0, 0, 0]

        a_time_device_distance_max_2 = [0, 0, 0, 0, 0]
        a_time_device_distance_count_2 = [0, 0, 0, 0, 0]
        a_time_device_distance_min_2 = [0, 0, 0, 0, 0]

        a_time_device_traffic_max_1 = [0, 0, 0, 0, 0]
        a_time_device_traffic_max_2 = [0, 0, 0, 0, 0]
        a_time_device_traffic_min_1 = [0, 0, 0, 0, 0]
        a_time_device_traffic_min_2 = [0, 0, 0, 0, 0]

        for a_test_user in all_test_user:
            interested_device = get_interested_device_type()
            # type_count +1
            a_time_device_type_count[interested_device - 1] += 1
            # print(a_time_device_type_count)
            # use_a1
            traffic_1, range_1 = a1(day, hour_, str(a_test_user), interested_device)
            # use_d2
            traffic_2, range_2 = a2(day, hour_, str(a_test_user), interested_device, 0.004)
            #
            a_time_traffics_by_1.append(traffic_1)
            a_time_traffics_by_2.append(traffic_2)
            #
            a_time_distance_by_1.append(range_1)
            a_time_distance_by_2.append(range_2)
            # 加上距離
            a_time_device_distance_count_1[interested_device - 1] += range_1
            a_time_device_distance_count_2[interested_device - 1] += range_2

            # set max 2
            set_max(a_time_device_distance_max_1, interested_device, range_1)
            set_max(a_time_device_distance_max_2, interested_device, range_2)
            set_min(a_time_device_distance_min_1, interested_device, range_1)
            set_min(a_time_device_distance_min_2, interested_device, range_2)

            # set max 1
            set_max(a_time_device_traffic_max_1, interested_device, traffic_1)
            set_max(a_time_device_traffic_max_2, interested_device, traffic_2)
            set_min(a_time_device_traffic_min_1, interested_device, traffic_1)
            set_min(a_time_device_traffic_min_2, interested_device, traffic_2)


        # calc avg
        a_time_device_distance_avg_1 = [0, 0, 0, 0, 0]
        set_avg(a_time_device_distance_count_1, a_time_device_type_count, a_time_device_distance_avg_1)

        a_time_device_distance_avg_2 = [0, 0, 0, 0, 0]
        set_avg(a_time_device_distance_count_2, a_time_device_type_count, a_time_device_distance_avg_2)

        sum_add(a_time_device_type_count, all_device_type_count)
        # add into global avg max min
        set_max_to_global(a_time_device_distance_max_1, y_axis_device_type_and_distance_max_1)
        set_max_to_global(a_time_device_distance_max_2, y_axis_device_type_and_distance_max_2)
        set_max_to_global(a_time_device_distance_min_1, y_axis_device_type_and_distance_min_1)
        set_max_to_global(a_time_device_distance_min_2, y_axis_device_type_and_distance_min_2)

        set_max_to_global(a_time_device_traffic_max_1, y_axis_device_type_and_traffic_max_1)
        set_max_to_global(a_time_device_traffic_max_2, y_axis_device_type_and_traffic_max_2)
        set_max_to_global(a_time_device_traffic_min_1, y_axis_device_type_and_traffic_min_1)
        set_max_to_global(a_time_device_traffic_min_2, y_axis_device_type_and_traffic_min_2)


        # print(a_time_device_traffic_max_1)
        # print(a_time_device_traffic_max_2)
        # print(a_time_device_traffic_min_1)
        # print(a_time_device_traffic_min_2)

        # print(a_time_device_distance_max_1)
        # print(a_time_device_distance_avg_1)
        # print(a_time_device_distance_min_1)
        # print("_____")
        # print(a_time_device_distance_max_2)
        # print(a_time_device_distance_avg_2)
        # print(a_time_device_distance_min_2)
        # print("_____1")



        #
        a_time_traffics_avg_by_1 = sum(a_time_traffics_by_1) / all_test_user_count
        a_time_traffics_avg_by_2 = sum(a_time_traffics_by_2) / all_test_user_count
        y_axis_traffic_avg_1.append(a_time_traffics_avg_by_1)
        y_axis_traffic_avg_2.append(a_time_traffics_avg_by_2)
        #
        a_time_distance_avg_by_1 = sum(a_time_distance_by_1) / all_test_user_count
        a_time_distance_avg_by_2 = sum(a_time_distance_by_2) / all_test_user_count
        y_axis_distance_avg_1.append(a_time_distance_avg_by_1)
        y_axis_distance_avg_2.append(a_time_distance_avg_by_2)


    #)
    y_axis_device_type_and_distance_max_1 = get_all_max_global(y_axis_device_type_and_distance_max_1)
    y_axis_device_type_and_distance_max_2 = get_all_max_global(y_axis_device_type_and_distance_max_2)
    y_axis_device_type_and_distance_min_1 = get_all_min_global(y_axis_device_type_and_distance_min_1)
    y_axis_device_type_and_distance_min_2 = get_all_min_global(y_axis_device_type_and_distance_min_2)

    y_axis_device_type_and_traffic_max_1 = get_all_max_global(y_axis_device_type_and_traffic_max_1)
    y_axis_device_type_and_traffic_max_2 = get_all_max_global(y_axis_device_type_and_traffic_max_2)
    y_axis_device_type_and_traffic_min_1 = get_all_min_global(y_axis_device_type_and_traffic_min_1)
    y_axis_device_type_and_traffic_min_2 = get_all_min_global(y_axis_device_type_and_traffic_min_2)




    # print("aaaaaaaaaaaaaa")
    # print(all_device_type_count)
    # print(y_axis_device_type_and_traffic_max_1)
    # print(y_axis_device_type_and_traffic_max_2)
    # print(y_axis_device_type_and_traffic_min_1)
    # print(y_axis_device_type_and_traffic_min_2)

    # print(x_axis)
    save_list_to_csv(x_axis, os.path.join(chart_data_save_path, "chart_1_5_x.csv"))
    # print(y_axis_traffic_avg_1)
    save_list_to_csv(y_axis_traffic_avg_1, os.path.join(chart_data_save_path, "chart_1_y1.csv"))
    # print(y_axis_traffic_avg_2)
    save_list_to_csv(y_axis_traffic_avg_2, os.path.join(chart_data_save_path, "chart_1_y2.csv"))
    # print(y_axis_distance_avg_1)
    save_list_to_csv(y_axis_distance_avg_1, os.path.join(chart_data_save_path, "chart_5_y1.csv"))
    # print(y_axis_distance_avg_2)
    save_list_to_csv(y_axis_distance_avg_2, os.path.join(chart_data_save_path, "chart_5_y2.csv"))

    save_list_to_csv(y_axis_device_type_and_distance_max_1, os.path.join(chart_data_save_path, "chart_6_y1_max.csv"))
    save_list_to_csv(y_axis_device_type_and_distance_max_2, os.path.join(chart_data_save_path, "chart_6_y2_max.csv"))
    save_list_to_csv(y_axis_device_type_and_distance_min_1, os.path.join(chart_data_save_path, "chart_6_y1_min.csv"))
    save_list_to_csv(y_axis_device_type_and_distance_min_2, os.path.join(chart_data_save_path, "chart_6_y2_min.csv"))

    save_list_to_csv(y_axis_device_type_and_traffic_max_1, os.path.join(chart_data_save_path, "chart_2_y1_max.csv"))
    save_list_to_csv(y_axis_device_type_and_traffic_max_2, os.path.join(chart_data_save_path, "chart_2_y2_max.csv"))
    save_list_to_csv(y_axis_device_type_and_traffic_min_1, os.path.join(chart_data_save_path, "chart_2_y1_min.csv"))
    save_list_to_csv(y_axis_device_type_and_traffic_min_2, os.path.join(chart_data_save_path, "chart_2_y2_min.csv"))


if __name__ == '__main__':
    select_day = 2
    select_hour = 4

    # data 1
    get_chart_1_data(select_day, select_hour)



    # test_the_number_of_users_and_traffic(select_day, select_hour)
