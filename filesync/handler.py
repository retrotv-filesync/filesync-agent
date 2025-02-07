"""
watchdog 라이브러리를 이용한 파일 시스템 이벤트 핸들러 클래스
"""
import sqlite3

from log import Log

from property import Property

from watchdog.events import (
    FileSystemEventHandler,
    FileDeletedEvent, FileCreatedEvent, FileModifiedEvent, FileMovedEvent,
    DirMovedEvent, DirCreatedEvent, DirDeletedEvent, DirModifiedEvent,
    FileClosedEvent, FileClosedNoWriteEvent, FileOpenedEvent
)

log = Log(__name__, filename="filesync.log").get_logger
db_config = Property("../config.ini", "DB").get_properties


class EventHandler(FileSystemEventHandler):
    """
    파일 시스템 이벤트 핸들러 클래스
    """

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        """
        파일이 생성되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 생성 이벤트
        :return: None
        """
        con = sqlite3.connect(db_config["db"])
        cur = con.cursor()

        if isinstance(event, FileCreatedEvent):
            log.info(f"파일이 생성되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'CREATE', 'F')")
        else:
            log.info(f"디렉터리가 생성되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'CREATE', 'D')")

        con.commit()
        con.close()

    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent) -> None:
        """
        파일이 삭제되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 삭제 이벤트
        :return: None
        """
        con = sqlite3.connect(db_config["db"])
        cur = con.cursor()

        if isinstance(event, FileDeletedEvent):
            log.info(f"파일이 삭제되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'DELETE', 'F')")
        else:
            log.info(f"디렉터리가 삭제되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'DELETE', 'D')")

        con.commit()
        con.close()

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        """
        파일이 수정되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 수정 이벤트
        :return: None
        """
        con = sqlite3.connect(db_config["db"])
        cur = con.cursor()

        if isinstance(event, FileModifiedEvent):
            log.info(f"파일이 수정되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'MODIFY', 'F')")
        else:
            log.info(f"디렉터리가 수정되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'MODIFY', 'D')")

        con.commit()
        con.close()

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        """
        파일이 이동되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 이동 이벤트
        :return: None
        """
        con = sqlite3.connect(db_config["db"])
        cur = con.cursor()

        if isinstance(event, FileMovedEvent):
            log.info(f"파일이 이동되었습니다: {event.src_path} -> {event.dest_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'MOVE', 'F')")
        else:
            log.info(f"디렉터리가 이동되었습니다: {event.src_path} -> {event.dest_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'MOVE', 'D')")

        con.commit()
        con.close()

    def on_closed(self, event: FileClosedEvent) -> None:
        """Called when a file opened for writing is closed.

        :param event:
            Event representing file closing.
        :type event:
            :class:`FileClosedEvent`
        """

        log.info(f"파일이 닫혔습니다: {event.src_path}")

    def on_closed_no_write(self, event: FileClosedNoWriteEvent) -> None:
        """Called when a file opened for reading is closed.

        :param event:
            Event representing file closing.
        :type event:
            :class:`FileClosedNoWriteEvent`
        """

        log.info(f"파일이 닫혔습니다: {event.src_path}")

    def on_opened(self, event: FileOpenedEvent) -> None:
        """Called when a file is opened.

        :param event:
            Event representing file opening.
        :type event:
            :class:`FileOpenedEvent`
        """

        log.info(f"파일이 열렸습니다: {event.src_path}")
