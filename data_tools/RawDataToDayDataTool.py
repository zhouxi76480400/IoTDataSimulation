from data_set.private_mobile_device_object import PrivateMobileDeviceObject
from data_tools import XYToMatrixTool


one_hour_seconds = 60 * 60

one_day_hours = 24


def raw_data_to_day_data(a_user_s_raw_data_list: list, day_count: int, start_timestamp: int):
    if a_user_s_raw_data_list is not None:
        # create new data list
        list_main = []
        for i in range(day_count):
            list_main.append([])
        # we need to get positions every hour of this user
        hour_count = day_count * one_day_hours
        for now_hour_not_include_days in range(hour_count):
            now_day = int(float(now_hour_not_include_days) / float(one_day_hours))
            now_hour = now_hour_not_include_days - one_day_hours * now_day
            now_hour_start_time_stamp = (now_hour * one_hour_seconds) + \
                                        (now_day * one_hour_seconds * one_day_hours) + start_timestamp
            now_hour_stop_time_stamp = now_hour_start_time_stamp + one_hour_seconds - 1
            # print("Day "+str(now_day+1) + " " + str(now_hour) + ":00 to " + str(now_hour) +
            #       ":59 " + "= " + str(now_hour_start_time_stamp) + " to " + str(now_hour_stop_time_stamp))
            # from data to find axis for every hour
            is_found = False
            x_position = -1.
            y_position = -1.
            i = 0
            # is out of this map
            # is_out_of_this_map = False
            for data in a_user_s_raw_data_list:
                data_object: PrivateMobileDeviceObject = data
                data_time_stamp_start = data_object.timestamp_start
                data_time_stamp_stop = data_object.timestamp_stop
                # print("\t data_pos=" + str(i) + ", timestamp start:" +
                #       str(data_time_stamp_start) + ", stop:" + str(data_time_stamp_stop))
                #
                if i == 0 and data_time_stamp_start > now_hour_stop_time_stamp:
                    # print("\t not in axis, skip..")
                    break
                #
                if now_hour_start_time_stamp <= data_time_stamp_start <= now_hour_stop_time_stamp:
                    x_position = data_object.x
                    y_position = data_object.y
                    is_found = True
                    # print("\t\t found tmp if1")
                #
                if now_hour_start_time_stamp <= data_time_stamp_stop <= now_hour_stop_time_stamp:
                    x_position = data_object.x
                    y_position = data_object.y
                    is_found = True
                    # print("\t\t found tmp if2")

                #
                if data_time_stamp_start > now_hour_stop_time_stamp:
                    # print("\t over than stop, skip..")
                    break

                i += 1

            # convert position to number
            number = 0
            if is_found:
                number = XYToMatrixTool.x_y_to_matrix(point_x=x_position, point_y=y_position)
            else:
                if now_hour_not_include_days > 0:
                    list_pos = now_day
                    data_pos = now_hour - 1
                    if now_hour == 0:
                        list_pos -= 1
                        data_pos = one_day_hours - 1
                    last_number = list_main[list_pos][data_pos]
                    if last_number > 0:
                        number = last_number
            # print("Get position:" + str(number))

            # add in to list
            list_main[now_day].append(number)
        return list_main
    return []
