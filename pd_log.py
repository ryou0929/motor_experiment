# from a import *
from module import *
import os
import datetime
import shutil
import matplotlib.pyplot as plt

if __name__ == '__main__':
    p = 20
    d = 5
    setup()

    omega_log = []
    theta_log = []
    tor_log = []
    time_log = []
    now = str(time.time())
    dir_pd = "log/p"+str(p)+"_d"+str(d)
    if os.path.exists(dir_pd):
        shutil.rmtree(dir_pd+"/")
    os.makedirs(dir_pd)
    log_dir_omega = dir_pd + "/"+"omega_p"+str(p)+"_d"+str(d)+".txt"
    log_dir_theta = dir_pd + "/"+"theta_p"+str(p)+"_d"+str(d)+".txt"
    log_dir_tor = dir_pd + "/"+"tor_p"+str(p)+"_d"+str(d)+".txt"
    log_dir_time = dir_pd + "/"+"time_p"+str(p)+"_d"+str(d)+".txt"
    log(log_dir_omega, datetime.datetime.now(), p, d)
    log(log_dir_theta, datetime.datetime.now(), p, d)
    log(log_dir_tor, datetime.datetime.now(), p, d)
    log(log_dir_time, datetime.datetime.now(), p, d)
    start_time = time.time()
    try:
        while 1:
            theta = B3M_readCmd(0, "theta")
            omega = B3M_readCmd(0, "omega")
            print(omega)
            tor = int(-p*theta) + int(-d * omega)
            log(log_dir_theta, theta)
            log(log_dir_omega, omega)
            log(log_dir_tor, tor)
            log(log_dir_time, time.time()-start_time)
            B3M_setTor(0, tor)
            theta_log.append(theta)
            omega_log.append(omega)
            tor_log.append(tor)
            time_log.append(time.time()-start_time)
    except:
        plt.plot(tor_log[:])
        plt.show()
