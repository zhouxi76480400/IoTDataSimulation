from data_set.private_mobile_device_object import PrivateMobileDeviceObject


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
