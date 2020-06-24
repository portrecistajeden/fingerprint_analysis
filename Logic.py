import cv2
import numpy as np


def convert_to_gray(image):
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image


def binarization(image, threshold):
    look_up_table = np.empty(256, np.uint8)

    for i in range(256):
        if i <= threshold:
            look_up_table[i] = 1
        else:
            look_up_table[i] = 0

    return cv2.LUT(image, look_up_table)


def otsu(image):
    image = convert_to_gray(image)
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist_norm = hist.ravel() / hist.sum()
    Q = hist_norm.cumsum()

    bins = np.arange(256)

    fn_min = np.inf
    thresh = -1

    for i in range(1, 256):
        p1, p2 = np.hsplit(hist_norm, [i])  # probabilities
        q1, q2 = Q[i], Q[255] - Q[i]  # cum sum of classes
        if q1 < 1.e-6 or q2 < 1.e-6:
            continue
        b1, b2 = np.hsplit(bins, [i])  # weights
        # finding means and variances
        m1, m2 = np.sum(p1 * b1) / q1, np.sum(p2 * b2) / q2
        v1, v2 = np.sum(((b1 - m1) ** 2) * p1) / q1, np.sum(((b2 - m2) ** 2) * p2) / q2
        # calculates the minimization function
        fn = v1 * q1 + v2 * q2
        if fn < fn_min:
            fn_min = fn
            thresh = i

    return binarization(image, thresh)


def K3M(image):
    a_values = [[3, 6, 7, 12, 14, 15, 24, 28, 30, 31, 48, 56, 60, 62, 63, 96, 112, 120,
                 124, 126, 127, 129, 131, 135, 143, 159, 191, 192, 193, 195, 199, 207, 223,
                 224, 225, 227, 231, 239, 240, 241, 243, 247, 248, 249, 251, 252, 253, 254],
                [7, 14, 28, 56, 112, 131, 193, 224],
                [7, 14, 15, 28, 30, 56, 60, 112, 120, 131, 135, 193, 195, 224, 225, 240],
                [7, 14, 15, 28, 30, 31, 56, 60, 62, 112, 120, 124, 131,
                 135, 143, 193, 195, 199, 224, 225, 227, 240, 241, 248],
                [7, 14, 15, 28, 30, 31, 56, 60, 62, 63, 112, 120, 124, 126, 131, 135, 143,
                 159, 193, 195, 199, 207, 224, 225, 227, 231, 240, 241, 243, 248, 249, 252],
                [7, 14, 15, 28, 30, 31, 56, 60, 62, 63, 112, 120, 124, 126, 131, 135, 143, 159, 191,
                 193, 195, 199, 207, 224, 225, 227, 231, 239, 240, 241, 243, 248, 249, 251, 252, 254]]

    look_up_table = np.zeros(256, np.uint8)
    for i in range(256):
        if i in a_values[0]:
            look_up_table[i] = 1

    kernel = np.array([[128, 1, 2],
                       [64, 0, 4],
                       [32, 16, 8]])

    kernel_altered = np.array([[128, 1, 2],
                               [64, 256, 4],
                               [32, 16, 8]])
    image = otsu(image)

    # expand image by 1 pixel border
    height = image.shape[0]
    width = image.shape[1]

    expand_zero = np.zeros((height+2, width+2), dtype=np.uint8)

    # insert original image within 0-filled matrix
    expand_zero[1:height+1, 1:width+1] = image

    # switch original image
    image = expand_zero

    while True:
        copy = image.copy()

        temp = cv2.filter2D(image, -1, kernel_altered, delta=-256)
        border = cv2.LUT(temp, look_up_table)

        for i in range(1, 6):
            indices = np.argwhere(border == 1)
            for (y, x) in indices:
                area = image[y-1:y+2, x-1:x+2]
                weight = np.sum(area * kernel)
                if weight in a_values[i]:
                    image[y, x] = 0
        if (image == copy).all():
            break

    indices = np.argwhere(image == 1)
    for (y, x) in indices:
        area = image[y - 1:y + 2, x - 1:x + 2]
        weight = np.sum(area * kernel)
        if weight in a_values[0]:
            image[y, x] = 0
    image = image[1:-1, 1:-1]
    result = np.where(image > 0, 0, 255).astype(np.uint8)
    result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
    return result


def detect_minutiae(image, minutiae_options):
    img = otsu(image)
    kernel = np.array([[1, 1, 1],
                       [1, 100, 1],
                       [1, 1, 1]])
    temp = cv2.filter2D(img, -1, kernel)

    flag = False
    single_point, edge_end, fork, crossing = [None]*4
    if minutiae_options[0] or minutiae_options[1] or minutiae_options[2] or minutiae_options[3]:
        if minutiae_options[0]:
            single_point = np.argwhere(temp == 100)
            if len(single_point) != 0:
                for item in single_point:
                    result = cv2.circle(image, (item[1], item[0]), 3, (51, 189, 255), 1)
                    if flag == False:
                        flag = True
            else:
                result = image

        if minutiae_options[2]:
            edge_end = np.argwhere(temp == 101)
            if len(edge_end) != 0:
                for item in edge_end:
                    result = cv2.circle(image, (item[1], item[0]), 3, (51, 87, 255), 1)
                    if flag == False:
                        flag = True
            else:
                result = image

        if minutiae_options[3]:
            fork = np.argwhere(temp == 103)
            if len(fork) != 0:
                for item in fork:
                    result = cv2.circle(image, (item[1], item[0]), 3, (51, 255, 219), 1)
                    if flag == False:
                        flag = True
            else:
                result = image

        if minutiae_options[1]:
            crossing = np.argwhere(temp == 104)
            if len(crossing) != 0:
                for item in crossing:
                    result = cv2.circle(image, (item[1], item[0]), 3, (51, 255, 117), 1)
                    if flag == False:
                        flag = True
            else:
                result = image
    else:
        result = image
    minucje = [single_point, edge_end, fork, crossing]
    return result, minucje, flag


def delete_false_minutiae(image, minutiae):
    # convert image to grayscale and select only one channel -> green
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows_values = np.count_nonzero(img == 0, axis=0)
    column_values = np.count_nonzero(img == 0, axis=1)

    low_pass = 0.05
    high_pass = 0.95

    rows_low_pass_index = find_percentage_index(rows_values, low_pass)
    rows_high_pass_index = find_percentage_index(rows_values, high_pass)
    cols_low_pass_index = find_percentage_index(column_values, low_pass)
    cols_high_pass_index = find_percentage_index(column_values, high_pass)

    image[cols_low_pass_index, rows_low_pass_index:rows_high_pass_index, :] = 127
    image[cols_high_pass_index, rows_low_pass_index:rows_high_pass_index, :] = 127
    image[cols_low_pass_index:cols_high_pass_index, rows_low_pass_index, :] = 127
    image[cols_low_pass_index:cols_high_pass_index, rows_high_pass_index, :] = 127

    filtered_minutiae = []
    for minutia_type in minutiae:
        if minutia_type is not None and minutia_type.shape[0] != 0:
            for minutia in minutia_type:
                if minutia[0] < cols_low_pass_index or minutia[0] > cols_high_pass_index or minutia[1] < rows_low_pass_index or minutia[1] > rows_high_pass_index:
                    filtered_minutiae.append(minutia)

    # change color of minutiae within border
    if filtered_minutiae is not None:
        for item in filtered_minutiae:
            result = cv2.circle(image, (item[1], item[0]), 3, (127, 127, 127), 2)
    return result


def find_percentage_index(arr, value):
    searched_values = value * np.sum(arr)
    temp = 0
    for index, value in enumerate(arr):
        temp += value
        if temp >= searched_values:
            break
    return index
