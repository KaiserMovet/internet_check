from datetime import datetime
import speedtest


class SpeedStatus():

    TIME_STR = "%Y.%m.%d - %H:%M:%S"

    def __init__(self, log_file):
        self.log_file = log_file
        pass

    def push_empty_entry(self):
        results_dict = {"download": 0, "upload": 0}
        entry = self._generate_entry(results_dict)
        self._save_info(entry)
        pass

    def speed_status(self):
        try:
            results_dict = self._speed_test()
        except:
            self.push_empty_entry()
            return
        entry = self._generate_entry(results_dict)
        self._save_info(entry)

    def _save_info(self, text):
        with open(self.log_file, 'a') as file:
            file.writelines([F'{text}\n'])

    @classmethod
    def _generate_entry(cls, results):
        time_log = datetime.now().strftime(cls.TIME_STR)
        # download speed in megabits
        download = round(results["download"] / 1000000, 1)
        # upload speed in megabits
        upload = round(results["upload"] / 1000000, 1)

        return F"[{time_log}] {download} {upload}"

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
