from interface.repository_interface import UserRepositoryInterface
from data.user_data import UserData
from werkzeug.exceptions import NotFound


class UserRepository(UserRepositoryInterface):
    def __init__(self, connection):
        self.conn = connection

    def get(self, username: str) -> UserData:
        # DBクライアントを作成する
        cursor = self.conn.cursor()

        # memo_idで検索を実行する
        query = "SELECT * FROM USERS WHERE name = %s"
        cursor.execute(query, [username])
        result: tuple = cursor.fetchone()

        # DBクライアントをcloseする
        cursor.close()

        if result is None:
            return None

        return UserData(id=result[0], name=result[1], hashed_password=result[2])

    def save(self, username: str, password: str):
        cursor = self.conn.cursor()

        from library.certification import get_password_hash
        hashed_password = get_password_hash(password)

        query = "INSERT INTO USERS (name, hashed_password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))

        # DBクライアントをcloseする
        cursor.close()

        return True

    def exist(self, username: str) -> bool:
        pass
