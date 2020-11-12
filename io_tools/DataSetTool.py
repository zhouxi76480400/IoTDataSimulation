import os
from data_set.private_mobile_device_object import PrivateMobileDeviceObject


def get_file_path(file=__file__):
    return os.path.split(os.path.abspath(file))[0]


def sort_str_to_int(element: str):
    return int(element)


def sort_get_start_timestamp(element: PrivateMobileDeviceObject):
    return element.timestamp_start


def read_data_set(path=''):
    print("Read dataset now ...")
    return_user_id_list = None
    return_user_data_list = None
    if os.path.isfile(path):
        print("\tThe dataset file is: ")
        print("\t\t" + path)
        # read file
        data_set_file = open(path, mode="r")
        data_set_to_str = data_set_file.read()
        data_set_file.close()
        # split data
        all_data_col = data_set_to_str.split("\n")
        # delete the last element
        last_col_of_data_set = len(all_data_col) - 1
        if all_data_col[last_col_of_data_set] == '':
            all_data_col.pop(last_col_of_data_set)
        # delete title
        all_data_col.pop(0)
        print("\t" + str(len(all_data_col)) + " records found!")
        # split data by users
        print("\tSplit all data by users ...")
        user_dicts = {}
        for col_now in all_data_col:
            # split col data
            col_data_split = str.split(col_now, ',')
            # read data
            col_timestamp_start = int(col_data_split[0])
            col_timestamp_stop = int(col_data_split[1])
            col_id_user = col_data_split[2]
            col_x = float(col_data_split[3])
            col_y = float(col_data_split[4])
            # read exist user data from dicts
            user_data = user_dicts.get(col_id_user)
            # make new list is not exists
            if user_data is None:
                user_data = []
                user_dicts[col_id_user] = user_data
            # make new object
            new_object = PrivateMobileDeviceObject()
            new_object.id_user = col_id_user
            new_object.x = col_x
            new_object.y = col_y
            new_object.timestamp_start = col_timestamp_start
            new_object.timestamp_stop = col_timestamp_stop
            # add in to list
            user_data.append(new_object)
        # finish classification
        print("\t" + str(len(user_dicts)) + " users found!")
        # transform to list<list<Object>>
        #  sort user id list
        user_id_list = list(user_dicts.keys())
        user_id_list.sort(key=sort_str_to_int)
        #  create user data list
        user_data_list = []
        for user_id in user_id_list:
            user_data = user_dicts.get(user_id)
            user_data.sort(key=sort_get_start_timestamp)
            user_data_list.append(user_data)
        # clear
        user_dicts.clear()
        return_user_id_list = user_id_list
        return_user_data_list = user_data_list
    return return_user_id_list, return_user_data_list


def get_all_users_have_mobile_devices_type():
    file_path = os.path.join(os.path.join(os.path.split(get_file_path(__file__))[0], "data_set"),
                             "objects_description.csv")
    devices_data = []
    f_ = open(file_path, "r")
    csv = f_.read()
    f_.close()
    lines = csv.split("\n")
    if lines[len(lines) - 1] == '':
        lines.pop(len(lines) - 1)
    lines.pop(0)
    for line in lines:
        values = line.split(",")
        id_user = int(values[1])
        device_type = int(values[2])
        devices_data.append([id_user, device_type])

    all_users_devices_list = [] #

    for i in range(0, 4000):
        set_ = [False, False, False, False, False]
        for device in devices_data:
            if device[0] == i+1:
                device_type = device[1]
                if device_type <= len(set_):
                    set_[device_type - 1] = True
        all_users_devices_list.append(set_)
    return all_users_devices_list
