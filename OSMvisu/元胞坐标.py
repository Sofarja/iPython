import numpy as np
import math

# 计算两点之间距离
def cal_distance(x1, x2):
    x1 = tuple(map(math.radians, x1))
    x2 = tuple(map(math.radians, x2))
    r = 6378.137*1000
    a = x1[1]-x2[1]
    b = x1[0]-x2[0]
    temp = math.pow(math.sin(a/2), 2)+math.pow(math.sin(b/2),
                                               2)*math.cos(x1[1])*math.cos(x2[1])
    return 2*math.asin(math.sqrt(temp))*r


points = [(31.9144045, 118.844825), (31.913614, 118.8424507), (31.9135673, 118.8423102),
         (31.9124163, 118.8386119), (31.911965, 118.8350022), (31.9117771, 118.8313818),
         (31.9115372, 118.827813), (31.9113112, 118.8245725), (31.9044129, 118.8045796),
         (31.904504, 118.8058724), (31.904923, 118.8072671), (31.9066525, 118.8108171),
         (31.906881, 118.8112643), (31.907261, 118.8120433), (31.9076736, 118.812889),
         (31.9084877, 118.8146257), (31.9090215, 118.8157643), (31.9098138, 118.8181263),
         (31.9100233, 118.8184251), (31.9109705, 118.8212361), (31.9112437, 118.8220944),
         (31.9111344, 118.8243689), (31.9145975, 118.8447214), (31.9137909, 118.8423298),
         (31.9137435, 118.8422515), (31.9137221, 118.8421872), (31.9125212, 118.8385742),
         (31.9121891, 118.8367086), (31.9120624, 118.8349727), (31.9120616, 118.8349589),
         (31.9118526, 118.8313749), (31.9116532, 118.8278092), (31.9115074, 118.8247118),
         (31.9114802, 118.8245342)]

all_length = 0
for i in range(len(points) - 1):
    all_length = all_length + cal_distance(points[i], points[i+1])
num = all_length / 50

print(all_length)
print(num)

split_points = [points[0]]
s_lengths = [0]


# 计算每个元胞的经纬度
def split(points,inter_d):
    for i in range(len(points) - 1):
        length0 = cal_distance(points[i], points[i+1])
        total_length = cal_distance(points[i], points[i+1]) + s_lengths[i]
        split_n = int(total_length/inter_d)
        if split_n == 1:
            lens = inter_d - s_lengths[i]
            split_points.append((points[i][0] + (points[i + 1][0] - points[i][0]) * lens / length0,
                                 points[i][1] + (points[i + 1][1] - points[i][1]) * lens / length0))
            s_lengths.append(total_length - inter_d)
        if split_n > 1:
            for j in range(1, split_n + 1 ):
                lens = (j * inter_d - s_lengths[i])
                split_points.append((points[i][0] + (points[i+1][0] - points[i][0]) * lens / length0,
                                     points[i][1] + (points[i+1][1] - points[i][1]) * lens / length0))
            s_lengths.append(total_length - split_n * inter_d)
        if split_n < 1:
            s_lengths.append(total_length)
    return split_points

endpoints = split(points,50)

all_length1 = 0
for i in range(len(endpoints) - 1):
    all_length1 = all_length1 + cal_distance(endpoints[i], endpoints[i+1])

print(endpoints)
print(len(endpoints))
print(all_length1)
