from datetime import datetime
import requests
import time
from speed_status import SpeedStatus
from connection_status import ConnectionStatus

TARGET_ADDRESS = "http://google.com"
INTERVAL_STEP = 300
SPEED_CHECK_STEP = 3
LOG_FILE = 'log.txt'
SPEED_LOG_FILE = 'speed_log.txt'


def main():

    connection_status = ConnectionStatus(TARGET_ADDRESS, LOG_FILE)
    speed_status = SpeedStatus(SPEED_LOG_FILE)
    index = -1
    while True:
        index = (index + 1) % SPEED_CHECK_STEP
        time.sleep(INTERVAL_STEP)
        has_connection = connection_status.loop()
        if index == 0:
            if has_connection:
                speed_status.speed_status()
            else:
                speed_status.push_empty_entry()


if __name__ == "__main__":
    main()
