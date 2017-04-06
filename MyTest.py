from pykalman import KalmanFilter
kf = KalmanFilter(initial_state_mean=70, n_dim_obs=1)
measurements = [71.21, 72.12, 75.34, 72.1, 73.1, 71.3, 72.26]
print(kf.em(measurements, n_iter=5).filter(measurements)[0])

