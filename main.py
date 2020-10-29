from io_tools import DataSetTool
from io_tools import CSVTool
from data_tools import DataProcessTool
import os

data_set_directory_name = "data_set"
data_set_file_name = "private_mobile_devices.csv"
# the path to dataset
data_set_file_path = os.path.join(os.path.join(DataSetTool.get_file_path(__file__), data_set_directory_name),
                                  data_set_file_name)
# the file name of summary form
summary_form_name = "summary"

simulation_time_day = 10  # days

start_timestamp = 0  #


def main():
    # Read dataset to python object
    user_id_list, user_data_list = DataSetTool.read_data_set(data_set_file_path)
    # Make a summary form
    CSVTool.make_a_summary_form(summary_form_name, user_id_list, user_data_list)
    # Check the global timestamp min and the global timestamp max to find 10 days start timestamp and end timestamp.
    # (seconds)
    global_timestamp_min, global_timestamp_max = \
        DataProcessTool.get_global_timestamp_min_and_timestamp_max(user_data_list)
    # check the timestamp range is in the simulation time
    simulation_time_seconds = 60 * 60 * 24 * simulation_time_day
    if (global_timestamp_max - global_timestamp_min) <= simulation_time_seconds:
        # we can continue
        start_timestamp = global_timestamp_min
        print("Set the first day's 0:00 to timestamp:" + str(start_timestamp))


    else:
        # we cannot continue
        print("The dataset is over ranged")


if __name__ == '__main__':
    main()
