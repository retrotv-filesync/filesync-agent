import time
import sqlite3
import configparser

from watchdog.observers import Observer
from filesync.EventHandler import EventHandler


properties = configparser.ConfigParser()
properties.read("../config.ini")


def create_table():
    db_config = properties["DB"]

    con = sqlite3.connect(db_config["db"])
    cur = con.cursor()
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

    path_config = properties["PATH"]

    paths = [
        path_config["paths"],
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
