import requests
from datetime import datetime


class ConnectionStatus():

    TIME_STR = "%Y.%m.%d - %H:%M:%S"
    HAS_CONNECTION_STR = "There is connection"
    HAS_NO_CONNECTION_STR = "There is no connection"

    def __init__(self, target, log_file):
        self.target = target
        self.log_file = log_file

        # generate first entry
        self.last_time = datetime.now()
        self.last_status = self._check_connection()
        start_entry = self._generate_entry(
            self.last_status, self.last_time)
        self._save_info(start_entry)
        # generate entry, which will be updated
        entry = self._generate_entry(
            self.last_status, self.last_time)
        self._save_info(entry)

    def loop(self):
        """
        return connection status
        """
        current_status = self._check_connection()
        current_time = datetime.now()
        entry = self._generate_entry(
            self.last_status, current_time)
        self._update_info(entry)

        # if status was changed
        if self.last_status != current_status:
            entry = self._generate_entry(
                current_status, current_time)
            self._save_info(entry)
            self.last_time = current_time
            self.last_status = current_status
        return current_status

    @classmethod
    def _generate_entry(cls, has_connection, current_time):
        time_log = current_time.strftime(cls.TIME_STR)
        if has_connection:
            has_connection_log = cls.HAS_CONNECTION_STR
        else:
            has_connection_log = cls.HAS_NO_CONNECTION_STR
        return F"[{time_log}] {has_connection_log}"

    def _check_connection(self):
        try:
            requests.get(self.target)
            cur_status = True
        except:
            cur_status = False
        return cur_status

    def _save_info(self, text):
        with open(self.log_file, 'a') as file:
            file.writelines([F'{text}\n'])

    def _update_info(self, text):
        with open(self.log_file, 'r') as file:
            all_lines = file.readlines()
        all_lines[-1] = F'{text}\n'
        with open(self.log_file, 'w') as file:
            file.writelines(all_lines)
