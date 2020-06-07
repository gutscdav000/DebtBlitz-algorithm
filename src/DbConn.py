import psycopg2 as psy, math



class DbConn:

    def __init__(self, host, db, user, password):
        try:
            self._conn = psy.connect(host=host, database=db, user=user, password=password)
        except Exception as e:
            print(e)

    @property
    def conn(self):
        return self._conn

    def execute_query(self, sql, commit = False):
        ''' executes a sql statement. commit's the transaction when commit=True'''
        with self._conn.cursor() as curs:
            try:
                curs.execute(sql, commit)
            except Exception as e:
                print("an error occurred:\n %s", e)
                return None
            if commit:
                self._conn.commit()
            else:
                return curs.fetchall()

    def close_conn(self):
        try:
            self._conn.close()
        except Exception as e:
            print(e)
        else:
            return self._conn.close == 1