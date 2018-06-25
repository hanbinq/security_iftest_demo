import pymysql.cursors
from pymysql.err import ProgrammingError
import os
import configparser as cparser

# ================= Reading db_config.ini setting ======
base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()

cf.read(file_path)
host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")


# ============ MySql base operating ===============
class DB:

    def __init__(self):
        try:
        # Connect to the database
            self.connection = pymysql.connect(host=host,
                                              port=int(port),
                                              user=user,
                                              password=password,
                                              db=db,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def clear(self, table_name):
        real_sql = "delete from " + table_name + ";"
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.connection.commit()

        # insert sql statement

    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        # print(real_sql)

        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)

        self.connection.commit()

        # select sql

    def select(self, table_name, where=None):
        sql_where = ""
        if where is not None:
            for key, value in where.items():
                sql_where = sql_where + str(key) + "=" + str(value) + ' AND '
            real_sql = "SELECT * FROM " + table_name + " WHERE " + sql_where[:-4] + ";"
            print(real_sql)
            with self.connection.cursor() as cursor:
                cursor.execute(real_sql)
                result = cursor.fetchall()
        else:
            real_sql = "SELECT * FROM " + table_name + ";"
            with self.connection.cursor() as cursor:
                print(real_sql)
                cursor.execute(real_sql)
                result = cursor.fetchall()
        return result

        # close database

    def close(self):
        self.connection.close()

        # init data

    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()

if __name__ == '__main__':
    db = DB()
    table_name = "mz_luck_user"
    data = {'lottery_num': 0, 'realname': '胡胡', 'order_num': 1, 'use_num': 0, 'phone': '18638945149', 'used_num': 0,
            'mid': 132, 'luid': 1, 'lid': 1}
    db.clear(table_name)  # 清空表数据
    db.insert(table_name, data)  # 重新插入表数据

    result = db.select("mz_luck_user", {'lid': 1, 'mid': 132})  # 查询表数据，多个条件之间默认 AND 连接
    print(result)
    db.close()






