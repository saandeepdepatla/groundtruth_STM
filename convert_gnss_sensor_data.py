import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

data_file1 = "/Users/saandeep/Desktop/convert_data_gnss_tocsv/Auto_STA8090_v4.7.10_D1_Nmea_18.12.18_12.49.35.txt"
data_file2 = "/Users/saandeep/Desktop/convert_data_gnss_tocsv/Auto_STA8090_v4.7.10_D1_Nmea_18.12.18_13.03.00.txt"
data_file3 = "/Users/saandeep/Desktop/convert_data_gnss_tocsv/Auto_STA8090_v4.7.10_D1_Nmea_18.12.18_13.07.16.txt"
gps_data_st = "/Users/saandeep/Desktop/convert_data_gnss_tocsv/gps_data_st.csv"
gyro_data_st = "/Users/saandeep/Desktop/convert_data_gnss_tocsv/gyro_data_st.csv"
accel_data_st = "/Users/saandeep/Desktop/convert_data_gnss_tocsv/accel_data_st.csv"


def convert_to_normal_lat_lon(lat_dd, lon_dd):
    lat_dd = float(lat_dd[0:2]) + float(lat_dd[2:]) / 60.
    lon_dd = float(lon_dd[0:3]) + float(lon_dd[3:]) / 60.
    return str(lat_dd), str(lon_dd)


def find_closest_gpgga_report(time_stamp):
    gpgga_msgs_sorted_keys = list(gpgga_msgs.keys())
    closet_index = np.searchsorted(gpgga_msgs_sorted_keys, time_stamp)
    return gpgga_msgs[gpgga_msgs_sorted_keys[closet_index]][0], gpgga_msgs[gpgga_msgs_sorted_keys[closet_index]][1]


def convert_to_utc_from_hhmmsss_format(time_stamp):
    return time_until_the_exp_day + float(time_stamp[0:2]) * 3600000.0 + float(time_stamp[2:4]) * 60000.0 + float(time_stamp[4:]) * 1000.0


def convert_to_utc_from_gps_time(week_number, time_of_the_week):
    return (week_number * 86400 * 7 + time_of_the_week) * 1000 + 315964800000 - 18000


f1 = open(data_file1, 'r')
lines1 = f1.readlines()
f1.close()

f2 = open(data_file1, 'r')
lines2 = f2.readlines()
f2.close()

f3 = open(data_file3, 'r')
lines3 = f3.readlines()
f3.close()

lines = lines1 + lines2 + lines3

time_cpu = []
gpgga_msgs = {}
for line in lines3:
    parts = line.split(',')
    if parts[0] == '$GPGGA':
        gpgga_msgs[float(parts[1])] = [parts[8], parts[9]]

gps_rows = []
gyro_rows = []
accel_rows = []

week_number_exp_day = 0
time_of_the_week_exp_day = 0
for line in lines3:
    parts = line.split(',')
    if parts[0] == '$PSTMTG':
        week_number_exp_day = float(parts[1])
        time_of_the_week_exp_day = float(parts[2])
        cpu_time = float(parts[4]) / 1000.
        gps_time_utc = convert_to_utc_from_gps_time(week_number_exp_day, time_of_the_week_exp_day)
        time_offset = gps_time_utc - cpu_time - 23000
        break

time_until_the_exp_day = (week_number_exp_day * 86400 * 7 + int(time_of_the_week_exp_day / 86400.) * 86400) * 1000 \
                         + 315964800000 - 18000


# time1 = []
# time2 = []
# for line in lines3:
#     parts = line.split(',')
#     if parts[0] == '$GPRMC':
#         time1.append(float(convert_to_utc_ms(parts[1])))
#     if parts[0] == '$PSTMDRSENMSG' and parts[1] == '31':
#         time2.append(float(parts[2]) / 1000.)
# time_offset = time1[0] - time2[0]
searching_gps = 0
searching_gga = 0
row = [0] * 8
gps_time = []
gyro_time = []
accel_time = []
for line in lines3:
    gyro_row = []
    accel_row = []
    #gps_row = []
    parts = line.split(',')
    # if parts[0] == '$GPRMC':
    #     row.append(int(convert_to_utc_from_hhmmsss_format(parts[1])))
    #     time_cpu.append(float(parts[1]))
    #     lat, lon = convert_to_normal_lat_lon(parts[3], parts[5])
    #     if parts[4] == 'S':
    #         lat = '-'+lat
    #     if parts[6] == 'W':
    #         lon = '-'+lon
    #     row.append(lat)
    #     row.append(lon)
    #     hacc, alt = find_closest_gpgga_report(float(parts[1]))
    #     row.append(alt)
    #     row.append(str(float(parts[7])*1.15078))  # converting the speed from knots to mph
    #     row.append(parts[8])
    #     row.append(hacc)
    #     row.append('gps')
    #     gps_rows.append(row)

    if (searching_gps == 1 or searching_gga == 1) and (parts[0] == '$PSTMDRGPS' or parts[0] == '$GPRMC'):
        if parts[0] == '$PSTMDRGPS':
            row[1] = parts[1]
            row[2] = parts[2]
            row[3] = parts[11].split('*')[0]
            row[4] = math.sqrt(float(parts[3]) ** 2 + float(parts[4]) ** 2)
            row[6] = float(parts[6]) * 20
            row[7] = 'gps'
            searching_gps = 0
            if searching_gps ==0 and searching_gga == 0:
                gps_rows.append(row)
                continue
        if parts[0] == '$GPRMC':
            row[5] = parts[8]
            searching_gga = 0
            if searching_gps ==0 and searching_gga == 0:
                gps_rows.append(row)
                continue
    # if parts[0] == '$GPGGA':
    #     gps_row.append(int(convert_to_utc_from_hhmmsss_format(parts[1])))
    #     lat, lon = convert_to_normal_lat_lon(parts[2], parts[4])
    #     if parts[3] == 'S':
    #         lat = '-'+lat
    #     if parts[5] == 'W':
    #         lon = '-'+lon
    #     gps_row.append(lat)
    #     gps_row.append(lon)
    #     gps_row.append(parts[9])
    #     gps_row.append(parts[9])
    #     gps_row.append(parts[9])
    #     gps_row.append(parts[8])
    #     gps_row.append('10')
    #     gps_row.append('gps')
    #     gps_rows.append(gps_row)

    if parts[0] == '$GPGGA':
        row = [0] * 8
        row[0] = int(convert_to_utc_from_gps_time(float(parts[1]), float(parts[2])))
        gps_time.append(float(row[0]))
        searching_gga = 1
        searching_gps = 1
        continue

    if parts[0] == '$PSTMDRSENMSG' and parts[1] == '31':
        gyro_row.append(str(int(float(parts[2]) / 1000. + time_offset)))
        gyro_time.append((int(float(parts[2]) / 1000. + time_offset)))
        gyro_row.append(float(parts[3]) * 4375. * 10**-6 * 0.0174533)
        gyro_row.append(float(parts[4]) * 4375. * 10**-6 * 0.0174533)
        gyro_row.append(float(parts[5].split('*')[0]) * 4375 * 10**-6 * 0.0174533)
        gyro_rows.append(gyro_row)

    if parts[0] == '$PSTMDRSENMSG' and parts[1] == '30':
        accel_row.append(str(int(float(parts[2]) / 1000. + time_offset)))
        accel_time.append((int(float(parts[2]) / 1000. + time_offset)))
        accel_row.append(float(parts[3]) * 61. * 10**-5)
        accel_row.append(float(parts[4]) * 61. * 10**-5)
        accel_row.append(float(parts[5].split('*')[0]) * 61 * 10**-5)
        accel_rows.append(accel_row)



init_row = ['utc', 'lat', 'lon', 'alt', 'speed', 'course', 'hor_acc', 'provider']
with open(gps_data_st, mode='w') as csv_file:
    write = csv.writer(csv_file)
    write.writerow(init_row)
    for row in gps_rows:
        write.writerow(row)

init_row = ['epoch', 'x', 'y', 'z']
with open(gyro_data_st, mode='w') as csv_file:
    write = csv.writer(csv_file)
    write.writerow(init_row)
    for row in gyro_rows:
        write.writerow(row)

with open(accel_data_st, mode='w') as csv_file:
    write = csv.writer(csv_file)
    write.writerow(init_row)
    for row in accel_rows:
        write.writerow(row)

# df = pd.read_csv(gps_data_st)
# time_gps = list(df["utc"])[0]
#
# df = pd.read_csv(gyro_data_st)
# time_gyro = list(df["epoch"])[0]
#
# time_offset = time_gyro - time_gps
#
# df = pd.read_csv(gyro_data_st)
# df["epoch"] += int(time_offset)
# df.to_csv(gyro_data_st, index=False)
#
# df = pd.read_csv(accel_data_st)
# df["epoch"] += int(time_offset)
# df.to_csv(accel_data_st, index=False)




# df = pd.read_csv(gps_data_st)
# df.sort_values("utc")
# df.to_csv(gps_data_st, index=False)
#
# df = pd.read_csv(accel_data_st)
# df.sort_values("epoch")
# df.to_csv(accel_data_st, index=False)
#
# df = pd.read_csv(gyro_data_st)
# df.sort_values("epoch")
# df.to_csv(gyro_data_st, index=False)



plt.figure()
plt.plot(np.diff(accel_time))
plt.show()







