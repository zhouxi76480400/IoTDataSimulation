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


def similarity_row_a_and_row_b(row_a: list, row_b: list, is_euclidean=False):
    return_data = 0
    sum_ = 0
    if len(row_a) == len(row_b):
        i = 0
        for element_from_a in row_a:
            element_from_b = row_b[i]
            if is_euclidean:
                x1 = element_from_a[0]
                x2 = element_from_b[0]
                y1 = element_from_a[1]
                y2 = element_from_b[1]
                euclidean_distance_xy1_xy2 = math.sqrt(math.pow((x1-x2), 2) + math.pow((y1-y2), 2))
                sum_ += euclidean_distance_xy1_xy2
            else:
                sum_ += (element_from_a * element_from_b)
            i += 1
    if not is_euclidean:
        return_data = math.cos(sum_)
    else:
        return_data = sum_ / len(row_a)
    return return_data


#  will return average and []
def similarity_matrix_a_and_matrix_b(matrix_a: list, matrix_b: list, is_random=False, is_euclidean=False):
    return_num = 0
    distance_count = []
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

            cos_a_and_b = similarity_row_a_and_row_b(list_a, list_b, is_euclidean=is_euclidean)
            distance_count.append(cos_a_and_b)
            cos_sum += cos_a_and_b

        similarity = cos_sum / list_size_a
        return_num = similarity
    return return_num, distance_count


def classification_all_users_from_result_matrix(mat: list):
    print(mat)
