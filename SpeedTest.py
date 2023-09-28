# import speedtest module
import speedtest
import datetime
import csv
import time


def bytes_to_mb(bytes):
    KB = 1024 # One Kilobyte is 1024 bytes
    MB = KB * 1024 # One MB is 1024 KB
    return int(bytes/MB)


test_start = datetime.datetime.now()
test_start_yyyymmddhhmmss = test_start.strftime('%y-%m-%d %H:%M:%S')
print('{:=^80s}\n'.format("Starting Speed Test - {}".format(test_start_yyyymmddhhmmss)))

year_start = test_start.year
month_start = test_start.month
day_start = test_start.day

with open('BradleyBurrell_Speedtest_{}{}{}.csv'.format(year_start, month_start, day_start), 'w', newline='') as csvfile:
    fieldnames = ['Date', 'Time', 'Download Speed (Mbps)', 'Upload Speed (Mbps)', 'Note']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    close_of_play = False
    while close_of_play is False:
        datetime_start = datetime.datetime.now()
        if datetime_start.minute not in {0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55}:
            time.sleep(1)
        else:
            print("Starting Test at {}".format(datetime_start))
            datetime_date = datetime_start.strftime('%y-%m-%d')
            datetime_time = datetime_start.strftime('%H:%M:%S')
            note = None

            speed_test = speedtest.Speedtest()

            try:
                download_speed = bytes_to_mb(speed_test.download())
                print("\tYour Download speed is {} Mbps".format(download_speed))
            except:
                download_speed = None
                note = 'Download Speed - ERROR: Unable to connect to servers to test latency'
                print("+++ {} +++".format(note))

            try:
                upload_speed = bytes_to_mb(speed_test.upload())
                print("\tYour Upload speed is {} Mbps".format(upload_speed))
            except:
                upload_speed = None
                note = 'Upload Speed - ERROR: Unable to connect to servers to test latency'
                print("+++ {} +++".format(note))
            datetime_end = datetime.datetime.now()
            print("Ending Test at {}\n".format(datetime_end))

            writer.writerow({'Date': datetime_date,
                             'Time': datetime_time,
                             'Download Speed (Mbps)': download_speed,
                             'Upload Speed (Mbps)': upload_speed,
                             'Note': note})
            time.sleep(120)
            speed_test = None
        if datetime_start.hour == 17:
            close_of_play = True

test_end = datetime.datetime.now()
test_end_yyyymmddhhmmss = test_end.strftime('%y-%m-%d %H:%M:%S')
print('{:=^80s}'.format("Ending Speed Test - {}".format(test_end_yyyymmddhhmmss)))