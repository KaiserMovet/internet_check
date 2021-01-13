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
        new_obj = []
        new_obj.append(all_obj[0])
        for i, obj in enumerate(all_obj[1:-1], 1):
            next_obj = all_obj[i + 1]
            last_obj = new_obj[-1]
            if obj.status != next_obj.status and \
                    (obj.date - last_obj.date).total_seconds() / 60 > 10:
                new_obj.append(obj)
        new_obj.append(all_obj[-1])
        self._save_to_db(new_obj)
