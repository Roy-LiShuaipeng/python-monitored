import psycopg2


class DBHelper:

    def __init__(self):

        # 初始化SQL
        self.SQL = 'SELECT "backend_start", "state_change", "datid", "datname",  \
                           "pid", "state", "client_addr",  "query" \
                    FROM "pg_stat_activity" \
                    WHERE "datname" = \'ag_simple\' \
                    ORDER BY "backend_start" DESC \
                    ;'
        self.connection_config = []

    def create_connection(self, connection_config):
        # 创建数据库连接
        self.connection_config = connection_config

    def get_data(self):
        # 创建数据库连接
        connection = psycopg2.connect(
            host=self.connection_config[0],
            port=self.connection_config[1],
            database=self.connection_config[2],
            user=self.connection_config[3],
            password=self.connection_config[4]
        )

        # 执行sql
        cur = connection.cursor()
        cur.execute(self.SQL)

        # 获取结果集
        data = cur.fetchall()

        # 关闭连接
        connection.close()

        return data


