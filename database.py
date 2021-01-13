from mysql.connector.errors import InterfaceError
import mysql.connector
import yaml
from contextlib import contextmanager
from speed_status import SpeedStatusObj
from connection_status import ConnectionStatusObj


class DataBase:
    CONFIG_FILE = "database.cfg"

    def __init__(self):
        with open(self.CONFIG_FILE, 'r') as f:
            content = f.read()
        content_dict = yaml.load(content, Loader=yaml.FullLoader)

        self.database = content_dict["database"]
        self.user = content_dict["user"]
        self.password = content_dict["password"]
        self.host = content_dict["host"]

    @contextmanager
    def _get_db(self):
        mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        try:
            yield mydb
        finally:

            mydb.close()

    def _execute_sql(self, sql_list):
        results = None
        with self._get_db() as mydb:
            mycursor = mydb.cursor()
            try:
                for sql_vars in sql_list:
                    mycursor.execute(*sql_vars)
            except Exception as ex:
                print(ex)
            else:
                try:
                    results = mycursor.fetchall()
                except InterfaceError:
                    results = None
                mydb.commit()
            finally:
                mycursor.close()
        return results

    def _get_save_tuple(self, content_obj):
        sql_values = ','.join(['%s'] * len(content_obj.FIELDS))
        sql = F"INSERT INTO {content_obj.DATABASE_NAME} "\
              F"({','.join(content_obj.FIELDS)}) "\
              F"VALUES ({sql_values})"
        return (sql, content_obj.get_tuple())

    def save(self, content_obj):
        sql_tuple = self._get_save_tuple(content_obj)
        self._execute_sql([sql_tuple])

    def save_multiple(self, content_obj_list):
        sql_list = []
        for content_obj in content_obj_list:
            sql_list.append(self._get_save_tuple(content_obj))
        self._execute_sql(sql_list)

    def get_last_entry(self, database_name, datefield_name):
        sql = F"SELECT * from {database_name} "\
              F"ORDER BY {datefield_name} DESC LIMIT 1"
        return (self._execute_sql([[sql]]))

    def update_last_entry(self, content_obj, datefield_name):
        remove_sql = F"DELETE FROM {content_obj.DATABASE_NAME} "\
                     F"order by {datefield_name} desc limit 1"
        all_sql = [[remove_sql], self._get_save_tuple(content_obj)]
        self._execute_sql(all_sql)

    def getAllSpeedStatus(self):
        sql = F"SELECT * from {SpeedStatusObj.DATABASE_NAME} "\
              F"ORDER BY {SpeedStatusObj.FIELDS[0]}"
        res = self._execute_sql([[sql]])
        obj_list = []
        for r in res:
            obj_list.append(SpeedStatusObj(*r[1:], r[0]))
        return obj_list

    def delete_all(self, database_name):
        sql = F"DELETE  from {SpeedStatusObj.DATABASE_NAME} "
        self._execute_sql([[sql]])
