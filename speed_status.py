from datetime import datetime
import speedtest


class SpeedStatusObj():
    DATABASE_NAME = 'internet_check_internetspeed'
    FIELDS = ['date', 'upload', 'download']

    def __init__(self, date, upload, download, id=None):
        self.date = date
        self.upload = round(upload, 1)
        self.download = round(download, 1)
        self.id = id

    def get_tuple(self):
        return (self.date.strftime("%Y-%m-%d - %H:%M:%S"), self.upload,
                self.download)

    def __repr__(self):
        return F"ConnectionSpeed<{self.id}, {self.date}, {self.upload}, {self.download}>"


class SpeedStatus():

    TIME_STR = "%Y.%m.%d - %H:%M:%S"

    def __init__(self, db):
        self.db = db
        pass

    def push_empty_entry(self, current_time):
        entry = SpeedStatusObj(current_time, 0, 0)
        self._save_info(entry)

    def speed_status(self, current_time):
        try:
            results_dict = self._speed_test()
        except:
            self.push_empty_entry()
            return
        entry = self._generate_entry(results_dict, current_time)
        self._save_info(entry)

    def _save_info(self, entry):
        self.db.save(entry)

    @staticmethod
    def _generate_entry(results, current_time):

        # download speed in megabits
        download = round(results["download"] / 1000000, 1)
        # upload speed in megabits
        upload = round(results["upload"] / 1000000, 1)

        return SpeedStatusObj(current_time, upload, download)

    @staticmethod
    def _speed_test():

        servers = []
        threads = None

        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download(threads=threads)
        s.upload(threads=threads)
        s.results.share()

        return s.results.dict()


def main():
    pass


if __name__ == "__main__":
    main()
