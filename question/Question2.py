
from math import sin, cos, tan
import numpy as np
import matplotlib.pyplot as plt

from tools import Compute, Data


''' GPS不准，process不准/未知？
    PF，lidar，landmark'''
''' bicycle model
    steering wheel angle-->front tire angle-->turn angle
'''
yaw_init = 3.00
wheelbase = 0.003  # km

data_length = 15000
second_series, velocity_series, wheel_angle_series, longitude_series, latitude_series\
    = Data.load_data(data_length, correction=1.3, conversion=17)
longitude_pre_list = [longitude_series[0]]
latitude_pre_list = [latitude_series[0]]
yaw_pre_list = [yaw_init]

print('start')
for i in range(data_length - 1):  # predict less first
    dt = second_series[i + 1] - second_series[i]
    distance = velocity_series[i] * dt  # km

    # print(i, 'steering angle', steering_angle_series[i])
    # bicycle model
    if abs(wheel_angle_series[i]) > 0.000001:  # is turn?    1d=0.017rad
        # 方向盘转角-->车辆转向角
        turn_angle = distance / wheelbase * tan(wheel_angle_series[i])   # rad, wheelbase?
        turn_radius_km = wheelbase / tan(wheel_angle_series[i])     # km
        turn_radius_lo = Compute.km_lo(turn_radius_km, latitude_series[i])
        turn_radius_la = Compute.km_la(turn_radius_km)
        # print('turn: ', turn_angle)

        longitude_pre = longitude_pre_list[i] - turn_radius_lo * sin(yaw_pre_list[i]) \
                        + turn_radius_lo * sin(yaw_pre_list[i] + turn_angle)
        latitude_pre = latitude_pre_list[i] + turn_radius_la * cos(yaw_pre_list[i])\
                       - turn_radius_la * cos(yaw_pre_list[i] + turn_angle)
        yaw_pre = yaw_pre_list[i] + turn_angle
        # print('yaw', i+1, ': ', yaw_pre)
    else:  # no turn
        longitude_pre = longitude_pre_list[i] + Compute.km_lo(
            (distance * cos(yaw_pre_list[i])), latitude_series[i])
        latitude_pre = latitude_pre_list[i] + Compute.km_la(
            (distance * sin(yaw_pre_list[i])))
        yaw_pre = yaw_pre_list[i]

    longitude_pre_list.append(longitude_pre)
    latitude_pre_list.append(latitude_pre)
    yaw_pre_list.append(yaw_pre)
print('end')

print('longitude rmse: ', Compute.root_mean_square_error(longitude_series, longitude_pre_list))
print('latitude rmse', Compute.root_mean_square_error(latitude_series, latitude_pre_list))

plt.scatter(longitude_series, latitude_series, label='measure')
plt.scatter(longitude_pre_list, latitude_pre_list, label='predict')
landmarks = np.array([[117.2675, 39.1180], [117.2685, 39.1180], [117.2695, 39.1210], [117.2775, 39.1190],
                      [117.3005, 39.1160], [117.2995, 39.1160], [117.2985, 39.1160], [117.2975, 39.1160],
                      [117.3005, 39.1170], [117.2995, 39.1170], [117.2985, 39.1170], [117.2975, 39.1170]])
# [117.274, 39.125], [117.261, 39.126], [117.257, 39.150], [117.269, 39.147]
plt.scatter(landmarks[:, 0], landmarks[:, 1], marker='s', s=60)
plt.legend()
# plt.xlim(*(117.21, 117.31))
# plt.ylim(*(39.11, 39.21))
plt.show()


