from data_set.private_mobile_device_object import PrivateMobileDeviceObject
import math
import random


def get_global_timestamp_min_and_timestamp_max(user_data_list: list):
    global_timestamp_min: int = 0
    global_timestamp_max: int = 0
    if user_data_list is not None:
        # set default value
        global_timestamp_min = user_data_list[0][0].timestamp_start
        global_timestamp_max = user_data_list[0][0].timestamp_stop
        for a_user_data_list in user_data_list:
            for a_user_data in a_user_data_list:
                a_user_data_object: PrivateMobileDeviceObject = a_user_data
                # set min
                if a_user_data_object.timestamp_start < global_timestamp_min:
                    global_timestamp_min = a_user_data_object.timestamp_start
                # set max
                if a_user_data_object.timestamp_stop > global_timestamp_max:
                    global_timestamp_max = a_user_data_object.timestamp_stop
    return global_timestamp_min, global_timestamp_max


def similarity_row_a_and_row_b(row_a: list, row_b: list):
    sum_ = 0
    if len(row_a) == len(row_b):
        i = 0
        for element_from_a in row_a:
            element_from_b = row_b[i]
            sum_ += (element_from_a * element_from_b)
            i += 1
    cos_ = math.cos(sum_)
    return cos_


def similarity_matrix_a_and_matrix_b(matrix_a: list, matrix_b: list, is_random=False):
    return_num = 0
    list_size_a = len(matrix_a)
    list_size_b = len(matrix_b)

    if list_size_a == list_size_b:

        cos_sum = 0

        for i in range(list_size_a):
            list_a = matrix_a[i]
            list_b = None
            if is_random:
                random_ = random.randint(0, list_size_a - 1)
                list_b = matrix_b[random_]
            else:
                list_b = matrix_b[i]

            cos_a_and_b = similarity_row_a_and_row_b(list_a, list_b)
            cos_sum += cos_a_and_b

        similarity = cos_sum / list_size_a
        return_num = similarity
    return return_num
