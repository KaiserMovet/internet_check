from datetime import datetime
import requests
import time

from connection_status import ConnectionStatus

TARGET_ADDRESS = "http://google.com"
INTERVAL_STEP = 5
LOG_FILE = 'log.txt'


def main():

    connection_status = ConnectionStatus(TARGET_ADDRESS, LOG_FILE)

    while True:
        time.sleep(INTERVAL_STEP)
        connection_status.loop()


if __name__ == "__main__":
    main()
