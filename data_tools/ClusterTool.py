

# check this user in which cluster
# day 1,2,... hour 0,1,...,23
def find_user_in_which_cluster(mat, day: int, hour_: int, user: int):
    return_value = -1
    if day + 1 <= len(mat) and hour_ + 1 <= len(mat[0]):
        matrix_this_time = mat[day - 1][hour_]
        cluster = 0
        for now_ in range(len(matrix_this_time)):
            matrix_x_s = matrix_this_time[now_]
            if matrix_x_s[user - 1] is True:
                cluster = now_
        return_value = cluster
    return return_value


def find_all_users_in_this_cluster(mat, all_user_devices_type_list,
                                   day: int, hour_: int, cluster_position: int, device_type=-1):
    return_value = []
    if day + 1 <= len(mat) and hour_ + 1 <= len(mat[0]):
        matrix_this_time = mat[day - 1][hour_]
        user_is_in_this_cluster_list = matrix_this_time[cluster_position]
        for pos_ in range(len(user_is_in_this_cluster_list)):
            is_in = user_is_in_this_cluster_list[pos_]
            if is_in:
                return_value.append(pos_ + 1)

    #
    new_list_to_return = []
    if device_type != -1:
        for a_id_user in return_value:
            has = all_user_devices_type_list[a_id_user - 1][device_type - 1]
            if has:
                new_list_to_return.append(a_id_user)
        return new_list_to_return
    return return_value


def get_neighbor_clusters(output_x_size: int, output_y_size: int, now_cluster_position: int):
    neighbor_clusters = []
    if now_cluster_position <= output_x_size * output_y_size - 1:
        left_offset = int(now_cluster_position % output_x_size)  # 0 for left, 9 for right
        top_offset = int(now_cluster_position / output_y_size)  # 0 for top, 9 for bottom
        left = now_cluster_position - 1
        top = now_cluster_position - output_x_size
        right = now_cluster_position + 1
        bottom = now_cluster_position + output_x_size
        left_top = top - 1
        right_top = top + 1
        right_bottom = bottom + 1
        left_bottom = bottom - 1
        #
        no_left = False
        no_right = False
        no_top = False
        no_bottom = False
        tmp1 = left_offset - 1
        tmp2 = top_offset + 1
        if tmp1 < 0:
            no_left = True
        if tmp1 > output_x_size - 3:
            no_right = True
        if tmp2 < 0:
            no_top = True
        if tmp2 > output_y_size - 2:
            no_bottom = True
        if not no_left and not no_top and not no_right and no_bottom:
            #  0001
            bottom = -1
            left_bottom = -1
            right_bottom = -1
        elif not no_left and not no_top and no_right and not no_bottom:
            #  0010
            right = -1
            right_top = -1
            right_bottom = -1
        elif not no_left and not no_top and no_right and no_bottom:
            #  0011
            right = -1
            right_top = -1
            right_bottom = -1
            bottom = -1
            left_bottom = -1
        elif not no_left and no_top and not no_right and not no_bottom:
            #  0100
            top = -1
            left_top = -1
            right_top = -1
        elif not no_left and no_top and not no_right and no_bottom:
            #  0101
            top = -1
            left_top = -1
            right_top = -1
            bottom = -1
            left_bottom = -1
            right_bottom = -1
        elif not no_left and no_top and no_right and not no_bottom:
            #  0110
            top = -1
            left_top = -1
            right_top = -1
            right = -1
            right_bottom = -1
        elif not no_left and no_top and no_right and no_bottom:
            #  0111
            top = -1
            left_top = -1
            right_top = -1
            right = -1
            right_bottom = -1
            bottom = -1
            left_bottom = -1
        elif no_left and not no_top and not no_right and not no_bottom:
            #  1000
            left = -1
            left_top = -1
            left_bottom = -1
        elif no_left and not no_top and not no_right and no_bottom:
            #  1001
            left = -1
            left_top = -1
            left_bottom = -1
            bottom = -1
            right_bottom = -1
        elif no_left and not no_top and no_right and not no_bottom:
            #  1010
            left = -1
            left_top = -1
            left_bottom = -1
            right_top = -1
            right = -1
            right_bottom = -1
        elif no_left and not no_top and no_right and no_bottom:
            #  1011
            left = -1
            left_top = -1
            left_bottom = -1
            right_top = -1
            right = -1
            right_bottom = -1
            bottom = -1
        elif no_left and no_top and not no_right and not no_bottom:
            #  1100
            left = -1
            left_top = -1
            left_bottom = -1
            top = -1
            right_top = -1
        elif no_left and no_top and not no_right and no_bottom:
            #  1101
            left = -1
            left_top = -1
            left_bottom = -1
            top = -1
            right_top = -1
            bottom = -1
            right_bottom = -1
        elif no_left and no_top and no_right and not no_bottom:
            #  1110
            left = -1
            left_top = -1
            left_bottom = -1
            top = -1
            right_top = -1
            right = -1
            right_bottom = -1
        elif no_left and no_top and no_right and no_bottom:
            #  1111
            left = -1
            left_top = -1
            left_bottom = -1
            top = -1
            right_top = -1
            right = -1
            right_bottom = -1
            bottom = -1
        tmp_list_clusters = [left, top, right, bottom, left_top, right_top, right_bottom, left_bottom]
        for a_value_for_cluster in tmp_list_clusters:
            if a_value_for_cluster > -1:
                neighbor_clusters.append(a_value_for_cluster)
    return neighbor_clusters
