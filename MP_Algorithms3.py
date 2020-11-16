import Algorithms3
from multiprocessing import Pool
from multiprocessing import cpu_count
import time
import os


def run_func(now_day_, now_time_):
    print("Run: day " + str(now_day_) + ", time:" + str(now_time_))
    t_1, t_2, d_1, d_2 = Algorithms3.get_chart_1_data(now_day_, now_time_)

    sum_t_1 = sum(t_1)  #
    sum_t_2 = sum(t_2)  #

    mean_d_1 = Algorithms3.get_mean(d_1)  #
    mean_d_2 = Algorithms3.get_mean(d_2)  #

    print("Get data finished:" + str(now_day_) + "," + str(now_time_))
    return [sum_t_1, sum_t_2, mean_d_1, mean_d_2]


if __name__ == '__main__':
    day_hour = 24
    day_count = 2

    data_sum_t_1 = []
    data_sum_t_2 = []

    day_mean_d_1 = []
    day_mean_d_2 = []

    result_all = []

    # run mp
    # cpu_count = cpu_count()
    cpu_count = 8
    print("CPU Count:" + str(cpu_count))
    p = Pool(cpu_count)

    for day_ in range(1, 3):
        select_day = day_
        for hour_ in range(0, day_hour):
            select_hour = hour_
            result_all.append(p.apply_async(run_func, args=(select_day, select_hour,)))
    p.close()
    p.join()

    print("all sub processes exit")

    for i in range(len(result_all)):
        ret_obj = result_all[i]
        data_sum_t_1.append(ret_obj.get()[0])
        data_sum_t_2.append(ret_obj.get()[1])
        day_mean_d_1.append(ret_obj.get()[2])
        day_mean_d_2.append(ret_obj.get()[3])

    print(data_sum_t_1)
    print(data_sum_t_2)
    print(day_mean_d_1)
    print(day_mean_d_2)
    Algorithms3.save_list_to_csv(data_sum_t_1, os.path.join(Algorithms3.chart_data_save_path, "chart_4_y1.csv"))
    Algorithms3.save_list_to_csv(data_sum_t_2, os.path.join(Algorithms3.chart_data_save_path, "chart_4_y2.csv"))
    Algorithms3.save_list_to_csv(day_mean_d_1, os.path.join(Algorithms3.chart_data_save_path, "chart_8_y1.csv"))
    Algorithms3.save_list_to_csv(day_mean_d_2, os.path.join(Algorithms3.chart_data_save_path, "chart_8_y2.csv"))
