import requests
from datetime import datetime


class ConnectionStatusObj():
    DATABASE_NAME = 'internet_check_internetstatus'
    FIELDS = ['change_time', 'status']

    def __init__(self, date, status, id=None):
        self.date = date
        self.status = status

    def get_tuple(self):
        return (self.date.strftime("%Y-%m-%d - %H:%M:%S"), self.status)


class ConnectionStatus():

    def __init__(self, target, db):
        self.target = target
        self.db = db

    def loop(self, current_time):
        """
        return connection status
        """
        current_status = self._check_connection()
        entry = self._generate_entry(
            current_status, current_time)
        self._save_info(entry)

        return current_status

    @staticmethod
    def _generate_entry(has_connection, current_time):
        return ConnectionStatusObj(current_time, has_connection)

    def _check_connection(self):
        try:
            requests.get(self.target)
            cur_status = True
        except:
            cur_status = False
        return cur_status

    def _save_info(self, entry):
        result = self.db.get_last_entry(
            ConnectionStatusObj.DATABASE_NAME, ConnectionStatusObj.FIELDS[0])
        if not result or result[0][2] != entry.status:
            self.db.save(entry)
        else:
            self.db.update_last_entry(entry, ConnectionStatusObj.FIELDS[0])
