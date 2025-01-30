import time
import sqlite3

from watchdog.observers import Observer
from filesync.handler import EventHandler
from filesync.property import Property

db_config = Property("../config.ini", "DB").get_properties
path_config = Property("../config.ini", "PATH").get_properties


def create_table() -> None:
    con = sqlite3.connect(db_config["db"])
    cur = con.cursor()

    # FILESYNC_INFO 테이블이 존재하는지 확인
    cur.execute(
        """
        SELECT COUNT(*) FROM SQLITE_MASTER WHERE NAME = 'FILESYNC_INFO'
        """
    )
    is_exist = cur.fetchone()[0] == 1

    # FILESYNC_INFO 테이블이 존재하지 않으면 생성
    if not is_exist:
        cur.execute(
            """
            CREATE TABLE FILESYNC_INFO (
                FILEPATH TEXT,
                MODE TEXT,
                TYPE TEXT
            )
            """
        )

        con.commit()

    con.close()


if __name__ == "__main__":
    create_table()

    paths = [
        path_config["paths"]
    ]
    event_handler = EventHandler()
    observers = []

    for path in paths:
        observer = Observer()

        # recursive=True로 설정하면 하위 디렉터리까지 감시
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        observers.append(observer)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
    # 권한이 없을 때
    except PermissionError:
        pass
    # 파일이 없을 때
    except FileNotFoundError:
        pass
    # 재귀 호출이 너무 깊을 때
    except RecursionError:
        pass

    for observer in observers:
        observer.join()
