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

# def translate(img, vec):
#     w, h = img.shape
#     newImg = np.full((w + vec[0], h + vec[1]),255)
#     mask = [[1, 0, 0],
#             [0, 1, 0],
#             [0, 0, 1]]
#     start = time.time()
#     for i in range(w):
#         for j in range(h):
#             mask[0][2] = i
#             mask[1][2] = j
#             [x, y, z]= np.matmul(mask, vec)
#             newImg[x][y] = img[i][j]
#     end = time.time()
#     print (end - start)
#     return newImg

def scale(img, factor):
    w, h = img.shape
    newImg = np.zeros((int(math.ceil(w * factor)) + 1, int(math.ceil(h * factor))+1))
    vec = [factor, factor, 1]
    mask = [[1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]]
    start = time.time()

    i=0
    while(i < w):
        j=0
        while(j<h):
            mask[0][0] = i
            mask[1][1] = j
            [x, y, z]= np.matmul(mask, vec)
            x = int(round(x))
            y = int(round(y))
            if(factor > 1):
                newImg[int(round(x-factor)):x+1, int(round(y-factor)):y+1] = img[i][j]
            else:
                newImg[x][y] = img[i][j]
            j+=1
        i+=1
    end = time.time()
    print (end - start)
    return newImg

def rotate(img, angle):
    w, h = img.shape
    newImg = np.zeros((512, 512))
    mask = [[math.cos(math.radians(angle)), math.sin(math.radians(angle)), 0],
            [-math.sin(math.radians(angle)), math.cos(math.radians(angle)), 0],
            [0, 0, 1]]
    start = time.time()
    for i in range(w):
        for j in range(h):
            vec = [i, j, 1]
            [x, y, z]= np.matmul(mask, vec)
            newImg[int(round(x))%512][int(round(y))%512] = img[i][j]
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

def convolution(image, cb):
    editImg = image[:]
    editImg.setflags(write=1)
    height, width = editImg.shape
    i = 1;
    while (i < height - 1):
        j = 1
        while (j < width - 1):
            editImg[i][j] = cb(image[i - 1:i + 1, j - 1:j + 1])
            j+=1
        i += 1

    return editImg