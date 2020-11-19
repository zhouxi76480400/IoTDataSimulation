#  調整request 的百分比 來算出avg distance 和 avg cost 的區別

from multiprocessing import Pool
from multiprocessing import cpu_count
import random
import os
import Algorithms7


def get_users_by_random_x_percent(all_users_count, x_percent):
    a_ = int(all_users_count * x_percent)
    # a_ = 5
    # print(all_users_count)
    ret_ = random.sample(range(1, all_users_count), a_)
    return ret_


def run_func(ratio):
    selected_day = 2
    selected_hour = 8
    all_users = 4000
    all_test_user = get_users_by_random_x_percent(all_users, ratio)
    print("All " + str(len(all_test_user)) + " test users")

    func_traffic_1 = []
    func_traffic_2 = []

    func_distance_1 = []
    func_distance_2 = []

    for a_test_user in all_test_user:
        a_test_user_str = str(a_test_user)
        # 開始計算
        # 隨機一個興趣類型
        interested_device = Algorithms7.get_interested_device_type()

        traffic1, distance1 = \
            Algorithms7.a1(selected_day, selected_hour, interested_device)

        traffic2, distance2 = \
            Algorithms7.a2(selected_day, selected_hour, interested_device, 0.004)

        func_traffic_1.append(traffic1)
        func_traffic_2.append(traffic2)

        func_distance_1.append(distance1)
        func_distance_2.append(distance2)

    # 求平均
    func_traffic_1_avg = Algorithms7.get_avg_from_list(func_traffic_1)
    func_traffic_2_avg = Algorithms7.get_avg_from_list(func_traffic_2)

    func_distance_1_avg = Algorithms7.get_avg_from_list(func_distance_1)
    func_distance_2_avg = Algorithms7.get_avg_from_list(func_distance_2)

    # avg distance1 avg distance2 avg cost 1 avg cost2
    return func_distance_1_avg, func_distance_2_avg, func_traffic_1_avg, func_traffic_2_avg


if __name__ == '__main__':

    cpu_count = cpu_count()
    # cpu_count = 8
    print("CPU Count:" + str(cpu_count))
    p = Pool(cpu_count)

    result_all = []

    for i in range(8):
        requests_ratio = .1 * (i+1)
        print("Now ratio:" + str(requests_ratio))
        result_all.append(p.apply_async(run_func, args=(requests_ratio,)))
    p.close()
    p.join()

    global_distance_1 = []
    global_distance_2 = []

    global_cost_1 = []
    global_cost_2 = []

    # 整理
    for i in range(len(result_all)):
        ret_obj = result_all[i]
        distance_1 = ret_obj.get()[0]
        distance_2 = ret_obj.get()[1]

        global_distance_1.append(distance_1)
        global_distance_2.append(distance_2)

        cost_1 = ret_obj.get()[2]
        cost_2 = ret_obj.get()[3]

        global_cost_1.append(cost_1)
        global_cost_2.append(cost_2)

    print("gd1" + str(global_distance_1))
    print("gd2" + str(global_distance_2))
    print("gc1" + str(global_cost_1))
    print("gc2" + str(global_cost_2))
    Algorithms7.save_list_to_csv(global_distance_1, os.path.join(Algorithms7.chart_data_save_path, "chart_12_y1.csv"))
    Algorithms7.save_list_to_csv(global_distance_2, os.path.join(Algorithms7.chart_data_save_path, "chart_12_y2.csv"))
    Algorithms7.save_list_to_csv(global_cost_1, os.path.join(Algorithms7.chart_data_save_path, "chart_13_y1.csv"))
    Algorithms7.save_list_to_csv(global_cost_2, os.path.join(Algorithms7.chart_data_save_path, "chart_13_y2.csv"))

