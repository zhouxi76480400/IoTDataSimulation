

#  First, we will make a square matrix with var(matrix_with_and_height).
#  1
#  ^
#  │
#  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐    ┐
#  │ 91 │ 92 │ 93 │ 94 │ 95 │ 96 │ 97 │ 98 │ 99 │ 100│    │
#  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤    │
#  │ 81 │ 82 │ 83 │ 84 │ 85 │ 86 │ 87 │ 88 │ 89 │ 90 │    │
#  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤    │
#  │ 71 │ 72 │ 73 │ 74 │ 75 │ 76 │ 77 │ 78 │ 79 │ 80 │    │
#  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤    │
#  │ 61 │ 62 │ 63 │ 64 │ 65 │ 66 │ 67 │ 68 │ 69 │ 70 │    │
#  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤    │
#  │ 51 │ 52 │ 53 │ 54 │ 55 │ 56 │ 57 │ 58 │ 59 │ 60 │    │
#  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤    1
#  │ 41 │ 42 │ 43 │ 44 │ 45 │ 46 │ 47 │ 48 │ 49 │ 50 │    │
#  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤    │
#  │ 31 │ 32 │ 33 │ 34 │ 35 │ 36 │ 37 │ 38 │ 39 │ 40 │    │
#  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤    │
#  │ 21 │ 22 │ 23 │ 24 │ 25 │ 26 │ 27 │ 28 │ 29 │ 30 │    │
#  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤    │
#  │ 11 │ 12 │ 13 │ 14 │ 15 │ 16 │ 17 │ 18 │ 19 │ 20 │    │
#  ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤    │
#  │  1 │  2 │  3 │  4 │  5 │  6 │  7 │  8 │  9 │ 10 │    │
#  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘──> ┘
#  0                                                 1
#  └────────────────────────1────────────────────────┘
#   Like this.
#  Then we should calculate the position
def x_y_to_matrix(matrix_with_and_height: int = 10, point_x: float = 0., point_y: float = 0.):
    print("point x and y to position calculate")
    return_value = 0.
    if (0 <= point_x <= 1) and (0 <= point_y <= 1):
        # x_offset
        x_offset_tmp = point_x * matrix_with_and_height
        x_offset = int(x_offset_tmp)
        if x_offset_tmp % 1 > 0:
            x_offset += 1
        if x_offset > matrix_with_and_height:
            x_offset = matrix_with_and_height
        if x_offset <= 0:
            x_offset = 1
        # y_offset
        y_offset_tmp = point_y * matrix_with_and_height
        y_offset = int(y_offset_tmp) * matrix_with_and_height
        if y_offset < 0:
            y_offset = 0
        if y_offset > (matrix_with_and_height - 1) * matrix_with_and_height:
            y_offset = (matrix_with_and_height - 1) * matrix_with_and_height
        return_value = x_offset + y_offset
    print("point x=" + str(point_x) + ", y=" + str(point_y) + ", position=" + str(return_value))
    return return_value
