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

data_set_folders = ["data_from_day_4", "data_from_day_5"]

data_day_range = list(range(0, 23))

som_matrix_name = "matrix.csv"

test_values_list = []  # all matrix som

devices_type_list = DataSetTool.get_all_users_have_mobile_devices_type()

# selected_day = random.randint(0, 1)
selected_day = 1

# selected_hour = random.randint(0, 23)
selected_hour = 15


def clean_som():
    test_values_list.clear()


# 找一天的一個小時先把矩陣填滿
def read_data_from_folders(read_day, read_hour):
    day_folder = data_set_folders[read_day]
    hour_folder = str(read_hour)
    print("from: " + day_folder + ", hour: " + hour_folder)
    path_to_som_matrix = \
        os.path.join(workspace_path,
                     os.path.join(day_folder,
                                  os.path.join(
                                      hour_folder, som_matrix_name)))
    print("Path:\n\t" + path_to_som_matrix)
    f_ = open(path_to_som_matrix, "r")
    csv_file = f_.read()
    f_.close()
    csv_split = csv_file.split("\n")
    if csv_split[len(csv_split) - 1] == "":
        csv_split.pop(len(csv_split) - 1)
    for a_line in csv_split:
        all_values_this_line = a_line.split(",")
        all_values_this_line_list = []
        for a_value in all_values_this_line:
            all_values_this_line_list.append(bool(int(a_value)))
        test_values_list.append(all_values_this_line_list)


#  run it
read_data_from_folders(selected_day, selected_hour)


# 這個用戶在哪個聚類.返回聚類編號(0-99)數字,這個聚類裡的其他用戶id(list)
def find_user_in_which_cluster(user_name: str):
    this_cluster_all_user_except_this_user = []
    user_in_this_cluster = -1
    user_id = int(user_name)
    for cluster_number in range(len(test_values_list)):
        cluster = test_values_list[cluster_number]
        is_in_this_cluster: bool = cluster[user_id]
        if is_in_this_cluster:
            user_in_this_cluster = cluster_number
            #
            for i_ in range(len(cluster)):
                is_in = cluster[i_]
                if is_in and i_ != user_id:
                    this_cluster_all_user_except_this_user.append(i_)
            break
    return user_in_this_cluster, this_cluster_all_user_except_this_user


# 所有用戶的XY座標保存點
all_users_xy_list = []


# 獲取所有用戶的xy保存點
def read_all_user_s_x_y_list(day__=selected_day, hour__=selected_hour):
    if len(all_users_xy_list) == 0:
        file_path = os.path.join(
            os.path.join(
                os.path.join(workspace_path,
                             data_set_folders[day__ - 1]),
                str(hour__)),
            str(hour__) + ".csv")
        csv_x_y = ""
        f = open(file_path, "r")
        csv_x_y = f.read()
        f.close()
        lines = csv_x_y.split("\n")
        if lines[len(lines) - 1] == "":
            lines.pop(len(lines) - 1)
        for now_ in range(len(lines)):
            list_xy = lines[now_].split(",")
            all_users_xy_list.append((float(list_xy[0]), float(list_xy[1])))
    return all_users_xy_list


# 先讓program填滿用戶座標
read_all_user_s_x_y_list()


# 獲取用戶的座標
def get_a_user_s_xy(user_a_name: str):
    all_xy_list = read_all_user_s_x_y_list()
    x, y = all_xy_list[int(user_a_name)]
    return x, y


# 計算兩個用戶相差的距離
def calculate_the_user_s_between(user_a_name: str, user_b_name: str):
    # x
    user_a_x, user_a_y = get_a_user_s_xy(user_a_name)
    #
    user_b_x, user_b_y = get_a_user_s_xy(user_b_name)
    distance = \
        math.sqrt(math.pow(user_b_x - user_a_x, 2) + math.pow(user_b_y - user_a_y, 2))
    return distance


# 找最近的用戶 適用於方法2
def find_close_users(my_user_name: str, range_: float, interest_device_type: int):
    my_user_name_int = int(my_user_name)
    traffic_count = 0
    distance_list = []
    for user_tmp in range(len(read_all_user_s_x_y_list())):
        # 跳過自己
        if user_tmp == my_user_name_int:
            continue
        user_tmp_name = str(user_tmp)
        between_ = calculate_the_user_s_between(my_user_name, user_tmp_name)
        ccc1 = between_ <= range_
        if ccc1:
            traffic_count += 1
            c1 = ClusterTool.has_this_type_device(devices_type_list, user_tmp_name, interest_device_type)
            if c1:
                distance_list.append((user_tmp_name, between_))
    return distance_list, traffic_count


def sort_get_distance(close_user):
    return close_user[1]


# 第二種算法
def a2(my_user_name: str, interest_device_type: int, range_expand_each_time: float):
    traffic_counter = 0
    range_ = range_expand_each_time
    max_try_times = int(math.sqrt(2) / range_expand_each_time) + 1
    #
    close_users = []
    while len(close_users) < 1 and traffic_counter < max_try_times:
        close_users, traffic_counter_now = find_close_users(my_user_name, range_, interest_device_type)
        traffic_counter += traffic_counter_now
        range_ += range_expand_each_time
    close_users = sorted(close_users, key=sort_get_distance)
    nearest = math.sqrt(2)
    if len(close_users) != 0:
        # print("from B:" + str(close_users))
        nearest = close_users[0][1]
    return traffic_counter, nearest  # range_


def check_cluster_check_left_time(found_list):
    left_time = 0
    for bool_i in found_list:
        if not bool_i:
            left_time += 1
    return left_time


def add_into_hit_list(hit_list, found_list):
    for fff_ in found_list:
        hit_list[fff_] = True


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


def save_list_to_csv(list_, save_file_path):
    csv_a = ""
    for ele in list_:
        csv_a += str(ele) + "\n"
    fi = open(save_file_path, "w")
    fi.write(csv_a)
    fi.close()
    csv_a = None


# 把這個聚類中的所有相關的用戶都返回
def find_all_users_in_this_cluster(cluster_position: int, device_type=-1):
    return_value = []
    #
    matrix_this_time = test_values_list
    user_is_in_this_cluster_list = matrix_this_time[cluster_position]
    for pos_ in range(len(user_is_in_this_cluster_list)):
        is_in = user_is_in_this_cluster_list[pos_]
        if is_in:
            return_value.append(pos_)
    #
    if device_type != -1:
        check_and_remove_not_interested_device_type(return_value, device_type)
    return return_value


# 把沒有的類型刪掉
def check_and_remove_not_interested_device_type(_raw_list, interest_device_type: int):
    for i in range(len(_raw_list) - 1, -1, -1):
        user_tmp_name_int = _raw_list[i]
        user_tmp_name = str(user_tmp_name_int)
        c1 = ClusterTool.has_this_type_device(devices_type_list, user_tmp_name, interest_device_type)
        if not c1:
            del _raw_list[i]


def a1(my_user_name: str, interest_device_type: int):
    traffic = 1
    #
    hit_list = []
    for h_pos in range(100):
        hit_list.append(False)
    #
    first_cluster, neighbor_users = find_user_in_which_cluster(my_user_name)
    # 排除一下和設備類型無關的
    check_and_remove_not_interested_device_type(neighbor_users, interest_device_type)

    # first_cluster = ClusterTool.find_user_in_which_cluster(all_values_list, day, hour_, int(my_user_name))
    neighbors = [first_cluster]

    hit_list[first_cluster] = True
    #
    # neighbor_users = ClusterTool.find_all_users_in_this_cluster(all_values_list, devices_type_list, day, hour_,
    #                                                             first_cluster, interest_device_type)
    # if len(neighbor_users) == 1:
    #     if str(neighbor_users[0]) == my_user_name:
    #         neighbor_users = []

    if len(neighbor_users) == 0:
        while check_cluster_check_left_time(hit_list) > 0 and not len(neighbor_users) > 0:
            neighbors = algorithm1_sub1(hit_list, neighbors)
            # print(neighbors)
            for neighbor in neighbors:
                neighbor_users = find_all_users_in_this_cluster(neighbor, interest_device_type)
                # neighbor_users = \
                #     ClusterTool. \
                #         find_all_users_in_this_cluster(all_values_list,
                #                                        devices_type_list,
                #                                        day, hour_, neighbor, interest_device_type)
                traffic += 1
                if len(neighbor_users) > 0:
                    break
    range_list = []
    # print("aaaa:" + str(neighbor_users))
    if len(neighbor_users) > 0:
        for neighbor_user in neighbor_users:
            if neighbor_user != int(my_user_name):
                range_list.append(calculate_the_user_s_between(str(my_user_name), str(neighbor_user)))
        if len(range_list) == 0:
            print("用0")
            return traffic, 0
        else:
            # print("from A:"+ str(range_list))
            min_in_list = min(range_list)
            # print("from A min:"+ str(minlist))
            return traffic, min_in_list
    return traffic, -1


# 更新所有座標點
def update_all_user_s_position():
    day_tmp = random.randint(1, 2)
    hour_tmp = random.randint(0, 23)
    print("day_tmp:"+str(day_tmp) + ", hour_tmp:" + str(hour_tmp))
    all_users_xy_list.clear()
    read_all_user_s_x_y_list(day_tmp, hour_tmp)
    clean_som()
    read_data_from_folders(day_tmp-1, hour_tmp)

    # for a_user in range(len(all_users_xy_list)):
    #     new_x = random.uniform(0, 1)
    #     new_y = random.uniform(0, 1)
    #     all_users_xy_list[a_user] = (new_x, new_y)


# 重新更新 1
def clean_and_reload_all_position():
    all_users_xy_list.clear()
    read_all_user_s_x_y_list()


# 1 - 5 隨機一種設備
def get_interested_device_type():
    device_type = random.randint(1, 5)
    return device_type


# 隨機百分之10的用戶
def get_users_by_random_10_percent(all_users_count):
    a_ = int(all_users_count / 10)
    # a_ = 5
    # print(all_users_count)
    ret_ = random.sample(range(1, all_users_count), a_)
    return ret_


def get_avg_from_list(double_list: list):
    avg: float = 0.
    if len(double_list) > 0:
        tmp_float: float = 0.
        for ll in double_list:
            tmp_float += ll
        tmp_float /= len(double_list)
        avg = tmp_float
    return avg


def run_algorithm():
    now_user_value = 4000
    all_test_user = get_users_by_random_10_percent(now_user_value)
    all_test_user_count = len(all_test_user)

    a1_distance_list = []  # 距離1
    a2_distance_list = []  # 距離2

    # 開始循環
    for a_test_user in all_test_user:
        a_test_user_str = str(a_test_user)  # 現在的用戶
        interested_device = get_interested_device_type()  # 想要找的用戶的特徵
        traffic_1, distance_1 = a1(a_test_user_str, interested_device)
        traffic_2, distance_2 = a2(a_test_user_str, interested_device, 0.004)
        a1_distance_list.append(distance_1)
        a2_distance_list.append(distance_2)

    return a1_distance_list, a2_distance_list


if __name__ == '__main__':
    global_distance_avg_list_1 = []
    global_distance_avg_list_2 = []

    global_distance_max_list_1 = []
    global_distance_max_list_2 = []

    global_distance_min_list_1 = []
    global_distance_min_list_2 = []

    for_times = 3
    for i in range(for_times):
        clean_and_reload_all_position()  # 1
        times = i + 1  # 次數
        print(i)

        c_max_distance_1 = []
        c_max_distance_2 = []

        c_avg_distance_1 = []
        c_avg_distance_2 = []

        c_min_distance_1 = []
        c_min_distance_2 = []

        for j in range(times):
            print("\t" + str(j))
            # 重新移動
            update_all_user_s_position()  # 2.1
            # 計算
            a1_distance_list, a2_distance_list = run_algorithm()
            # 最大1
            max_distance_1 = max(a1_distance_list)
            # 平均1
            avg_distance_1 = get_avg_from_list(a1_distance_list)
            # 最小1
            min_distance_1 = min(a1_distance_list)

            # 最大2
            max_distance_2 = max(a2_distance_list)
            # 平均2
            avg_distance_2 = get_avg_from_list(a2_distance_list)
            # 最小2
            min_distance_2 = min(a2_distance_list)

            c_max_distance_1.append(max_distance_1)
            c_max_distance_2.append(max_distance_2)
            c_avg_distance_1.append(avg_distance_1)
            c_avg_distance_2.append(avg_distance_2)
            c_min_distance_1.append(min_distance_1)
            c_min_distance_2.append(min_distance_2)

        #  計算
        global_distance_max_list_1.append(max(c_max_distance_1))
        global_distance_max_list_2.append(max(c_max_distance_2))
        global_distance_avg_list_1.append(get_avg_from_list(c_avg_distance_1))
        global_distance_avg_list_2.append(get_avg_from_list(c_avg_distance_2))
        global_distance_min_list_1.append(min(c_min_distance_1))
        global_distance_min_list_2.append(min(c_min_distance_2))

    # save
    save_list_to_csv(global_distance_max_list_1, os.path.join(chart_data_save_path, "chart_11_y1_max.csv"))
    save_list_to_csv(global_distance_max_list_2, os.path.join(chart_data_save_path, "chart_11_y2_max.csv"))
    save_list_to_csv(global_distance_avg_list_1, os.path.join(chart_data_save_path, "chart_11_y1_avg.csv"))
    save_list_to_csv(global_distance_avg_list_2, os.path.join(chart_data_save_path, "chart_11_y2_avg.csv"))
    save_list_to_csv(global_distance_min_list_1, os.path.join(chart_data_save_path, "chart_11_y1_min.csv"))
    save_list_to_csv(global_distance_min_list_2, os.path.join(chart_data_save_path, "chart_11_y2_min.csv"))
