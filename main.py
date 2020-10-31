from io_tools import DataSetTool
from io_tools import CSVTool
from data_tools import DataProcessTool
from data_tools import RawDataToDayDataTool
from io_tools import DiskTool
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
        #
        # problem 1: convert matrix to 10 x (400 x 24)
        print("\nCalculating problem 1 ...")
        fin_list = []
        for i in range(simulation_time_day):
            fin_list.append([])
        for a_user_s_data in user_data_list:
            # convert raw data to day data
            a_result = RawDataToDayDataTool.raw_data_to_day_data(a_user_s_data, simulation_time_day, start_timestamp)
            for i in range(simulation_time_day):
                day_result = a_result[i]
                fin_list[i].append(day_result)
        # save to 10 matrix
        for i in range(simulation_time_day):
            now_list = fin_list[i]
            DiskTool.write_to_disk(os.path.join(DiskTool.create_output_directory(), "output_matrix_" +
                                                str(i + 1) + ".txt"), str(now_list))

        print("\tFinished! \n")

        # problem 2.1 (Md and M(d-1))
        print("\nCalculating problem 2.1 ...")
        for i in range(simulation_time_day):
            if i > 0:
                print("\tCalculating similarity between M" + str(i + 1) + " and M" + str(i) + " ...")
                similarity = DataProcessTool.similarity_matrix_a_and_matrix_b(fin_list[i], fin_list[i - 1])
                print("\t\t Result:" + str(similarity))

        print("\tFinished! \n")

        # problem 2.2 (Md and M(d-2))
        print("\nCalculating problem 2.2 ...")
        for i in range(simulation_time_day):
            if i > 1:
                print("\tCalculating similarity between M" + str(i + 1) + " and M" + str(i - 1) + " ...")
                similarity = DataProcessTool.similarity_matrix_a_and_matrix_b(fin_list[i], fin_list[i - 2])
                print("\t\t Result:" + str(similarity))

        print("\tFinished! \n")

        # problem 2.3 (Md and M(d-3))
        print("\nCalculating problem 2.3 ...")
        for i in range(simulation_time_day):
            if i > 2:
                print("\tCalculating similarity between M" + str(i + 1) + " and M" + str(i - 2) + " ...")
                similarity = DataProcessTool.similarity_matrix_a_and_matrix_b(fin_list[i], fin_list[i - 3])
                print("\t\t Result:" + str(similarity))

        print("\tFinished! \n")

        # problem 2.4 (Md and M(d-1) random)
        print("\nCalculating problem 2.4 (random) ...")
        for i in range(simulation_time_day):
            if i > 0:
                print("\tCalculating similarity between M" + str(i + 1) + " and M" + str(i) + " (random) ...")
                similarity = DataProcessTool.similarity_matrix_a_and_matrix_b(fin_list[i], fin_list[i - 1],
                                                                              is_random=True)
                print("\t\t Result:" + str(similarity))

        print("\tFinished! \n")

    else:
        # we cannot continue
        print("The dataset is over ranged")


if __name__ == '__main__':
    main()
