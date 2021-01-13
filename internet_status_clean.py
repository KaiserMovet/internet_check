from datetime import datetime
from connection_status import ConnectionStatusObj


class InternetStatusClean:
    pass

    def __init__(self, db):
        self.db = db

    def _save_to_db(self, new_obj):
        self.db.delete_all(ConnectionStatusObj.DATABASE_NAME)
        self.db.save_multiple(new_obj)
        pass

    def clean(self):
        all_obj = self.db.getAllConnectionStatus()
        print(all_obj)
        new_obj = []
        new_obj.append(all_obj[0])
        last_status = all_obj[0].status
        last_date = all_obj[0].date
        for obj in all_obj[1:]:
            if obj.status != last_status and \
               (obj.date - last_date).total_seconds() / 60 > 10:
                last_status = obj.status
                last_date = obj.date
                new_obj.append(obj)
        self._save_to_db(new_obj)
