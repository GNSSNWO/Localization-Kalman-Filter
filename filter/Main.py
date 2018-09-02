
import matplotlib.pyplot as plt

from tools import Data
from filter.Fusion import *


yaw_init = 3.00
wheelbase = 0.003  # km
dt = 0.02
data_length = 1300

# load data
_, _, _, true_longitude_series, true_latitude_series = Data.load_data(data_length)
second_series, velocity_series, wheel_angle_series, longitude_series, latitude_series\
    = Data.load_noise_data(data_length)

us = list(zip(velocity_series, wheel_angle_series))     # just for index 拿着用
# zs = list(zip(longitude_series, latitude_series))       # matrix operations
zs = []     # array([[longitude], [latitude]])
for (longitude, latitude) in zip(longitude_series, latitude_series):
    zs.append(array([[longitude], [latitude]]))

ekf_, predicts, estimates = run_localization(std_vel=0.01, std_steer=np.radians(0.01), std_lo=0.3, std_la=0.1,
                            us=us, zs=zs, dt=dt, wheelbase=wheelbase, data_length=data_length)

print('Final P:', ekf_.P.diagonal())
# plt.scatter(true_longitude_series, true_latitude_series, color='b', label='true')
plt.scatter(longitude_series, latitude_series, color='b', label='measure')
# plt.scatter(predicts[:, 0], predicts[:, 1],  color='r', label='predict')
plt.scatter(estimates[:, 0], estimates[:, 1],  color='y', label='estimate')
plt.title("EKF Robot localization")
plt.legend()
plt.show()


