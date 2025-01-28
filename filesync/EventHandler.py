import logging
import sqlite3
from watchdog.events import (
    FileSystemEventHandler,
    FileDeletedEvent, FileCreatedEvent, FileModifiedEvent, FileMovedEvent,
    DirMovedEvent, DirCreatedEvent, DirDeletedEvent, DirModifiedEvent,
    FileClosedEvent, FileClosedNoWriteEvent, FileOpenedEvent
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


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
        con = sqlite3.connect("filesync.db")
        cur = con.cursor()

        if isinstance(event, FileCreatedEvent):
            log.info(f"파일이 생성되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'C', 'F')")
        else:
            log.info(f"디렉터리가 생성되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'C', 'D')")

        con.commit()
        con.close()

    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent) -> None:
        """
        파일이 삭제되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 삭제 이벤트
        :return: None
        """
        con = sqlite3.connect("filesync.db")
        cur = con.cursor()

        if isinstance(event, FileDeletedEvent):
            log.info(f"파일이 삭제되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'D', 'F')")
        else:
            log.info(f"디렉터리가 삭제되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'D', 'D')")

        con.commit()
        con.close()

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        """
        파일이 수정되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 수정 이벤트
        :return: None
        """
        con = sqlite3.connect("filesync.db")
        cur = con.cursor()

        if isinstance(event, FileModifiedEvent):
            log.info(f"파일이 수정되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'M', 'F')")
        else:
            log.info(f"디렉터리가 수정되었습니다: {event.src_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'M', 'D')")

        con.commit()
        con.close()

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        """
        파일이 이동되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 이동 이벤트
        :return: None
        """
        con = sqlite3.connect("filesync.db")
        cur = con.cursor()

        if isinstance(event, FileMovedEvent):
            log.info(f"파일이 이동되었습니다: {event.src_path} -> {event.dest_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'M', 'F')")
        else:
            log.info(f"디렉터리가 이동되었습니다: {event.src_path} -> {event.dest_path}")
            cur.execute(f"INSERT INTO FILESYNC_INFO (FILEPATH, MODE, TYPE) VALUES ('{event.src_path}', 'M', 'D')")

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
