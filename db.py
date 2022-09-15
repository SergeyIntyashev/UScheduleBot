import sqlite3


class DBHelper:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.conn = sqlite3.connect('schedule.sqlite')
        self.__setup()

    def __del__(self):
        self.conn.close()
        self.__instance = None

    def __setup(self) -> None:
        stmt = 'CREATE TABLE IF NOT EXISTS users (id text)'
        self.conn.execute(stmt)
        self.conn.commit()

    def get_user_ids(self) -> list[str]:
        stmt = "SELECT id FROM users"
        res = self.conn.execute(stmt)
        return [user_info[0] for user_info in res.fetchmany()]

    def add_user(self, user_id: str) -> None:
        user_exist = self.user_exist(user_id)
        if not user_exist:
            stmt = "INSERT INTO users (id) VALUES (?)"
            args = (user_id,)
            self.conn.execute(stmt, args)
            self.conn.commit()

    def delete_user(self, user_id: str) -> None:
        user_exist = self.user_exist(user_id)
        if user_exist:
            stmt = "DELETE FROM users WHERE id = (?)"
            args = (user_id,)
            self.conn.execute(stmt, args)
            self.conn.commit()

    def user_exist(self, user_id) -> bool:
        stmt = "SELECT id FROM users WHERE id = (?)"
        args = (user_id,)
        res = self.conn.execute(stmt, args)
        return res.fetchone() is not None


db_helper = DBHelper()
