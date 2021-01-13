import time
from datetime import datetime
from speed_status import SpeedStatus, SpeedStatusObj
from connection_status import ConnectionStatus, ConnectionStatusObj
from internet_speed_cleen import InternetSpeedClean
from database import DataBase
import sys

TARGET_ADDRESS = "http://google.com"
INTERVAL_STEP = 5
SPEED_CHECK_STEP = 12


def loop():
    db = DataBase()
    connection_status = ConnectionStatus(TARGET_ADDRESS, db)
    speed_status = SpeedStatus(db)
    index = -1
    while True:
        current_time = datetime.now()
        index = (index + 1) % SPEED_CHECK_STEP
        has_connection = connection_status.loop(current_time)
        if index == 0:
            if has_connection:
                speed_status.speed_status(current_time)
            else:
                speed_status.push_empty_entry(current_time)
        time.sleep(INTERVAL_STEP)


def clean():
    db = DataBase()
    cleaner = InternetSpeedClean(db)
    cleaner.clean()


def load_from_file():
    db = DataBase()
    load_type = sys.argv[2]
    file_name = sys.argv[3]
    obj_to_save = []
    with open(file_name, 'r') as f:
        lines = f.readlines()

    if load_type == "speed":
        for line in lines:
            if not line:
                continue
            splitted_lines = line.split()
            download = float(splitted_lines[3])
            upload = float(splitted_lines[4])
            date_str = " ".join(splitted_lines[0:3])[1:-1]
            date = datetime.strptime(
                date_str, '%Y.%m.%d - %H:%M:%S')
            obj_to_save.append(SpeedStatusObj(date, upload, download))
        db.save_multiple(obj_to_save)

    elif load_type == "status":
        for line in lines:
            if not line:
                continue
            splitted_lines = line.split()
            date_str = " ".join(splitted_lines[0:3])[1:-1]
            date = datetime.strptime(
                date_str, '%Y.%m.%d - %H:%M:%S')
            status = bool("no" in line)
            obj_to_save.append(ConnectionStatusObj(date, status))
        db.save_multiple(obj_to_save)


def main():

    if sys.argv[1] == "loop":
        loop()
    elif sys.argv[1] == "clean":
        clean()
    elif sys.argv[1] == "load":
        load_from_file()


if __name__ == "__main__":
    main()
