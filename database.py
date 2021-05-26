"""this file contains the DataBase manager"""
from sqlite3 import connect, Connection, Cursor
from typing import Union, List
from contributor import AlbertUnruh


__all__ = (
    "DataBase",
    "DbUser",
)

TABLE_USER = "user"


class DataBase:
    """is the DataBase class"""

    contributor = [AlbertUnruh]

    def __init__(self, *, name: str = "database.sqlite"):
        self._connection: Connection = connect(name)
        self._cursor: Cursor = self._connection.cursor()

    def commit(self):
        """commits the statements to the DataBase"""
        self._connection.commit()

    def execute(self, cmd: Union[str, List[str]], *, autocommit=True):
        """executes a command"""

        if isinstance(cmd, str):
            cmd = [cmd]

        for raw in cmd:
            for c in raw.split(";"):
                self._cursor.execute(c)

        if autocommit:
            self.commit()

    def get_all(self, table, **query):
        """fetches all entries from a table with the given query"""
        if query:
            name, query = query.popitem()
            self._cursor.execute(f"""
SELECT * FROM {table} WHERE {name}=={query!r}
""")
        else:
            self._cursor.execute(f"""
SELECT * FROM {table}
""")
        return self._cursor.fetchall()

    def close(self):
        """closes the DB"""
        self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class DbUser:
    """is a special class for the User from the DataBase"""

    contributor = [AlbertUnruh]

    # for PyCharm
    # noinspection PyShadowingBuiltins
    @staticmethod
    def new_user(*, id: int, user: str, name: str, mail: str,
                 school: str, cl4ss: str, team: str):
        """adds a User to the DataBase"""
        with DataBase() as db:
            db.execute(f"""\
INSERT INTO {TABLE_USER!r} VALUES (
    {id!r},
    {user!r},
    {mail!r},
    {name!r},
    {school!r},
    {cl4ss!r},
    {team!r}
);
""")

    # for PyCharm
    # noinspection PyShadowingBuiltins
    @staticmethod
    def delete_user(*, id: int):
        """removes a User from the DataBase"""
        with DataBase() as db:
            db.execute(f"""\
DELETE FROM {TABLE_USER!r} WHERE id=={id!r};
""")

    @staticmethod
    def get_users(**query) -> list:
        """gets users by the query"""
        assert len(query.items()) == 1, "Please insert only ONE query!"
        with DataBase() as db:
            return db.get_all(TABLE_USER, **query)

    @staticmethod
    def get_all_users() -> list:
        """gets users by the query"""
        with DataBase() as db:
            return db.get_all(TABLE_USER)

    with DataBase() as db:
        db.execute(f"""\
CREATE TABLE IF NOT EXISTS {TABLE_USER!r} (
    'id'        INTEGER,
    'user'      TEXT,
    'mail'      TEXT,
    'name'      TEXT,
    'school'    TEXT,
    'cl4ss'     TEXT,
    'team'      TEXT
);
""")
