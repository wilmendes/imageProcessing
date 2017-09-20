import numpy as np
import time
import math

def histogram(image):
    h, w = image.shape
    hist = np.zeros(256, dtype='uint8')
    for i in range(h):
        for j in range(w):
            hist[image[i][j]] += 1
    return hist


def hist_draw(image):
    values = histogram(image)
    hist = np.empty((256, 256), dtype='uint8')
    hist[:] = 255
    h, w = hist.shape

    for i in range(w):
        for j in range(h):
            if j > h - values[i]:
                hist[j][i] = 0
    return hist

def avg(image):
    sum = np.sum(image)
    return sum / image.size


def variance(image):
    height, width = image.shape
    average = avg(image)
    totalSum = 0
    for i in range(height):
        for j in range(width):
            totalSum += (image[i][j] - average) ** 2
    return totalSum / (height * width)

def translate(img, vec):
    w, h = img.shape
    newImg = np.full((w + vec[0], h + vec[1]),255)
    mask = [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]
    start = time.time()
    for i in range(w):
        for j in range(h):
            mask[0][2] = i
            mask[1][2] = j
            [x, y, z]= np.matmul(mask, vec)
            newImg[x][y] = img[i][j]
    end = time.time()
    print (end - start)
    return newImg

def scale(img, factor):
    w, h = img.shape
    newImg = np.zeros((int(math.ceil(w * factor)) + 1, int(math.ceil(h * factor))+1))
    vec = [factor, factor, 1]
    mask = [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]
    start = time.time()
    for i in range(w):
        for j in range(h):
            mask[0][0] = i
            mask[1][1] = j
            [x, y, z]= np.matmul(mask, vec)
            newImg[int(math.ceil(x))][int(math.ceil(y))] = img[i][j]
    end = time.time()
    print (end - start)
    return newImg

def median(image):
    arr = np.copy(image)
    arr = np.asarray(arr).reshape(-1)
    arr.sort()
    return arr[len(arr) / 2]


def mode(image):
    hist = histogram(image)
    i, = np.where(hist==(max(hist)))
    return i


def count_lower(image, threshold):
    height, width = image.shape
    totalSum = 0

    for i in range(height):
        for j in range(width):
            if image[i][j] < threshold:
                totalSum += 1

    return totalSum


def count_higher(image, threshold):
    height, width = image.shape
    totalSum = 0
    for i in range(height):
        for j in range(width):
            if image[i][j] > threshold:
                totalSum += 1

    return totalSum


def apply_threshold(image, threshold, value, sign):
    height, width = image.shape
    for i in range(height):
        for j in range(width):
            if (image[i][j] > threshold and sign == 'gt') or\
               (image[i][j] < threshold and sign == 'lt') or\
               (image[i][j] == threshold and sign == 'eq'):
                image[i][j] = value

# image = cv2.imread('Lenna.png', 0)
# height, width = image.shape
#
# q1 = image[0:height / 2, 0:width / 2]
# q2 = image[0:height / 2, width / 2:width]
# q3 = image[height / 2:height, 0:width / 2]
# q4 = image[height / 2:height, width / 2:width]

# question 1
# hist_draw(q1)
# print('--------- Questao 1 -----------')
# print('b) ' + str(avg(q2)))
# print('c) ' + str(median(q3)))
# print('d) ' + str(mode(q4)))
# print('e) q1:' + str(variance(q1)))
# print('e) q2:' + str(variance(q2)))
# print('f) ' + str(count_lower(image[0:height/2, :], 100)))
# print('g) ' + str(count_higher(image[height/2:height, :], 150)))
#
# # question 2
# apply_threshold(q2, avg(q2) - 1, 255, 'gt') #-- a
# apply_threshold(q4, mode(q4)[0] - 1, 200, 'gt') #-- b
# apply_threshold(q3, median(q3) - 1, 220, 'gt') #-- c
# apply_threshold(q2, avg(q2), 100, 'gt') #-- d
# apply_threshold(q2, avg(q2), 0, 'gt') #-- e
# apply_threshold(q3, median(q3), 255, 'gt') #-- e
#
# cv2.imshow('q2', image)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()