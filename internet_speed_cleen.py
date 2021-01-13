from datetime import datetime
from speed_status import SpeedStatusObj


class InternetSpeedClean:
    pass

    def __init__(self, db):
        self.db = db

    def _get_grouped_data(self):
        all = self.db.getAllSpeedStatus()
        grouped_data = {}

        for entry in all:
            year = entry.date.year
            month = entry.date.month

            if year not in grouped_data:
                grouped_data[year] = {}
            if month not in grouped_data[year]:
                grouped_data[year][month] = []
            grouped_data[year][month].append(entry)
        return grouped_data

    def _save_to_db(self, new_speed_obj):
        self.db.delete_all(SpeedStatusObj.DATABASE_NAME)
        self.db.save_multiple(new_speed_obj)

    def clean(self):
        grouped_data = self._get_grouped_data()
        new_speed_obj = []
        current_time = datetime.now()
        for year in grouped_data.keys():
            for month in grouped_data[year].keys():
                if month == current_time.month and year == current_time.year:
                    new_speed_obj += grouped_data[year][month]
                    continue
                sum_upload = sum(
                    [entry.upload for entry in grouped_data[year][month]])
                avg_upload = round(
                    sum_upload / len(grouped_data[year][month]), 1)

                sum_download = sum(
                    [entry.download for entry in grouped_data[year][month]])
                avg_download = round(
                    sum_download / len(grouped_data[year][month]), 1)

                # Min values
                min_upload = min(
                    entry.upload for entry in grouped_data[year][month]
                    if entry.upload != 0)
                min_download = min(
                    entry.download for entry in grouped_data[year][month]
                    if entry.download != 0)

                # Max values
                max_upload = max(
                    entry.upload for entry in grouped_data[year][month])
                max_download = max(
                    entry.download for entry in grouped_data[year][month])

                start_date = grouped_data[year][month][0].date
                end_date = grouped_data[year][month][-1].date
                # Middle values
                middle_count = 3
                while True:

                    middle_upload = \
                        (avg_upload * middle_count - min_upload -
                         max_upload) / (middle_count - 2)
                    middle_download = \
                        (avg_download * middle_count -
                         min_download - max_download) / (middle_count - 2)
                    middle_upload = round(middle_upload, 1)
                    middle_download = round(middle_download, 1)

                    if (min_upload <= middle_upload <= max_upload and
                        min_download <= middle_download <= max_download) or \
                            middle_count > 20:

                        duration_beetwen_entries = \
                            (end_date - start_date) / (middle_count - 1)
                        # Save min
                        new_speed_obj.append(SpeedStatusObj(
                            start_date, min_upload, min_download))
                        # Save middle
                        for i in range(middle_count - 2):
                            middle_date = start_date + \
                                duration_beetwen_entries * (i + 1)
                            new_speed_obj.append(SpeedStatusObj(
                                middle_date, middle_upload, middle_download))
                        # Save max
                        new_speed_obj.append(SpeedStatusObj(
                            end_date, max_upload, max_download))
                        break

                    else:
                        middle_count += 1
                        continue

        self._save_to_db(new_speed_obj)
