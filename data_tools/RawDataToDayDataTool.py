from data_set.private_mobile_device_object import PrivateMobileDeviceObject

# def get_day_and_hour(start_timestamp: int, )


one_hour_seconds = 60 * 60

one_day_hours = 24


def raw_data_to_day_data(a_user_s_raw_data_list: list, day_count: int, start_timestamp: int):
    if a_user_s_raw_data_list is not None:
        # we need to get positions every hour of this user
        hour_count = day_count * one_day_hours
        for now_hour_not_include_days in range(hour_count):
            now_day = int(float(now_hour_not_include_days) / float(one_day_hours))
            now_hour = now_hour_not_include_days - one_day_hours * now_day
            now_hour_start_time_stamp = now_hour * one_hour_seconds + start_timestamp
            now_hour_stop_time_stamp = now_hour_start_time_stamp + one_hour_seconds - 1
            print("Day "+str(now_day+1) + " " + str(now_hour) + ":00 to " +str(now_hour) + ":59 " + "= " + str(now_hour_start_time_stamp) + " to " + str(now_hour_stop_time_stamp))

            # print("test" + str(now_hour))




        print(hour_count)




        # for a_user_s_raw_data in a_user_s_raw_data_list:
        #     raw_data: PrivateMobileDeviceObject = a_user_s_raw_data
        #     timestamp_start_tmp = raw_data.timestamp_start
        #     timestamp_stop_tmp = raw_data.timestamp_stop
        #
        #
        #     print("------start-------")
        #     print(str(timestamp_start_tmp) + "," + str(timestamp_stop_tmp))







        print(a_user_s_raw_data_list)

