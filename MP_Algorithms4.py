import Algorithms4
from multiprocessing import Pool
from multiprocessing import cpu_count
import time
import os


def run_func(now_day_, frequencies_):
    print("run_func: " + str(frequencies_))
    hour_list = [6]
    if frequencies_ == 2:
        hour_list = [11, 23]
    elif frequencies_ == 3:
        hour_list = [7, 15, 23]
    elif frequencies_ == 4:
        hour_list = [5, 11, 17, 23]
    #
    d_1_s = []
    d_2_s = []
    for now_hour in hour_list:
        t_1, t_2, d_1, d_2 = Algorithms4.get_chart_1_data(now_day_, now_hour)
        d_1_s.append(Algorithms4.get_mean(d_1))
        d_2_s.append(Algorithms4.get_mean(d_2))
    print("Get data finished:" + str(frequencies_))
    return [Algorithms4.get_mean(d_1_s), Algorithms4.get_mean(d_2_s)]


if __name__ == '__main__':
    day_hour = 24
    day_count = 2

    # data_sum_t_1 = []
    # data_sum_t_2 = []

    day_mean_d_1 = []
    day_mean_d_2 = []

    result_all = []

    # run mp
    # cpu_count = cpu_count()
    cpu_count = 8
    print("CPU Count:" + str(cpu_count))
    p = Pool(cpu_count)

    select_day = 1

    for _i in range(4):
        frequencies = _i + 1
        print("frequencies " + str(frequencies) + " each day")
        result_all.append(p.apply_async(run_func, args=(select_day, frequencies,)))
    p.close()
    p.join()

    print("all sub processes exit")

    for i in range(len(result_all)):
        ret_obj = result_all[i]
        # data_sum_t_1.append(ret_obj.get()[0])
        # data_sum_t_2.append(ret_obj.get()[1])
        day_mean_d_1.append(ret_obj.get()[0])
        day_mean_d_2.append(ret_obj.get()[1])

    # print(data_sum_t_1)
    # print(data_sum_t_2)
    print(day_mean_d_1)
    print(day_mean_d_2)
    # Algorithms3.save_list_to_csv(data_sum_t_1, os.path.join(Algorithms3.chart_data_save_path, "chart_4_y1.csv"))
    # Algorithms3.save_list_to_csv(data_sum_t_2, os.path.join(Algorithms3.chart_data_save_path, "chart_4_y2.csv"))
    Algorithms4.save_list_to_csv(day_mean_d_1, os.path.join(Algorithms4.chart_data_save_path, "chart_10_y1.csv"))
    Algorithms4.save_list_to_csv(day_mean_d_2, os.path.join(Algorithms4.chart_data_save_path, "chart_10_y2.csv"))
