from datetime import datetime
import requests
import time


TARGET_ADDRESS = "http://google.com"
INTERVAL = 300
LOG_FILE = 'log.txt'


def generate_entry(has_connection, current_time, last_time):
    time_log = current_time.strftime("%Y.%m.%d - %H:%M:%S")
    if has_connection:
        has_connection_log = "There was connection for"
    else:
        has_connection_log = "There was no connection for"
    time_with_con = (current_time - last_time)
    time_with_con_log = F"{time_with_con.days} days, "\
                        F"{time_with_con.seconds//3600} hours and "\
                        F"{(time_with_con.seconds//60)%60} minutes"
    return F"[{time_log}] {has_connection_log} {time_with_con_log}"


def generate_start_entry(current_status, current_time):
    time_log = current_time.strftime("%Y.%m.%d - %H:%M:%S")
    if current_status:
        has_connection_log = "There is connection"
    else:
        has_connection_log = "There is no connection"
    return F"[{time_log}] {has_connection_log}"


def save_info(text):
    with open(LOG_FILE, 'a') as file:
        file.writelines([F'{text}\n'])


def update_info(text):
    with open(LOG_FILE, 'r') as file:
        all_lines = file.readlines()
    all_lines[-1] = F'{text}\n'
    with open(LOG_FILE, 'w') as file:
        file.writelines(all_lines)


def check_connection():
    try:
        requests.get(TARGET_ADDRESS)
        cur_status = True
    except:
        cur_status = False
    return cur_status


def main():
    last_time = datetime.now()
    last_status = check_connection()
    # Generate start entry
    start_entry = generate_start_entry(last_status, last_time)
    save_info(start_entry)
    # Generate normal entry
    entry = generate_entry(last_status, last_time, last_time)
    save_info(entry)

    while True:
        time.sleep(INTERVAL)
        current_status = check_connection()
        current_time = datetime.now()
        entry = generate_entry(last_status, current_time, last_time)
        update_info(entry)

        # if status was changed
        if last_status != current_status:
            entry = generate_entry(current_status, last_time, last_time)
            save_info(entry)
            last_time = current_time
            last_status = current_status

        print(entry)


if __name__ == "__main__":
    main()
