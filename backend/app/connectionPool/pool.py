import mysql.connector.pooling

dbconfig = {
    "host": "localhost",
    "port": "3307",
    "user": "root",
    "password": "kerito17",
    "database": "SisNotas",
}

class MySQLPool:
    def __init__(self):             
        self.pool = self.create_pool(pool_name='task_pool', pool_size=3)

    def create_pool(self, pool_name, pool_size):
        pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_session=True,
            **dbconfig
        )
        return pool

    def close(self, conn, cursor):
        cursor.close()
        conn.close()

    def execute(self, sql, args=None, commit=False):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            if args:
                cursor.execute(sql, args)
            else:
                cursor.execute(sql)
            if commit:
                conn.commit()
            else:
                return cursor.fetchall()
        finally:
            self.close(conn, cursor)

    def executemany(self, sql, args, commit=False):
        conn = self.pool.get_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(sql, args)
            if commit:
                conn.commit()
        finally:
            self.close(conn, cursor)
