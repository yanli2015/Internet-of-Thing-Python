from pykalman import KalmanFilter
kf = KalmanFilter(initial_state_mean=70, n_dim_obs=1)
measurements = [71.21, 72.12, 75.34, 72.1, 73.1, 71.3, 72.26]
print(kf.em(measurements, n_iter=5).filter(measurements)[0])

# from numpy import *
# import matplotlib.pyplot as pyl
#
# x = [2.53240, 1.91110, 1.18430, 0.95784, 0.33158,
#      -0.19506, -0.82144, -1.64770, -1.87450, -2.2010]
#
# y = [-2.50400, -1.62600, -1.17600, -0.87400, -0.64900,
#      -0.477000, -0.33400, -0.20600, -0.10100, -0.00600]
#
# coefficients = polyfit(x, y, 6)
# polynomial = poly1d(coefficients)
# xs = arange(-2.2, 2.6, 0.1)
# ys = polynomial(xs)
#
# pyl.plot(x, y, 'o')
# pyl.plot(xs, ys)
# pyl.ylabel('y')
# pyl.xlabel('x')
# # pyl.show()
# pyl.savefig('./templates/foo.png')

