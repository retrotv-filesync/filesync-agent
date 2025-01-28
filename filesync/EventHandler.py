from watchdog.events import (
    FileSystemEventHandler,
    FileDeletedEvent, DirDeletedEvent,
    DirCreatedEvent, FileCreatedEvent,
    DirModifiedEvent, FileModifiedEvent,
    DirMovedEvent, FileMovedEvent
)


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
        if not event.is_directory:
            print(f"파일이 생성되었습니다: {event.src_path}")

    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent) -> None:
        """
        파일이 삭제되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 삭제 이벤트
        :return: None
        """
        if not event.is_directory:
            print(f"파일이 삭제되었습니다: {event.src_path}")

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        """
        파일이 수정되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 수정 이벤트
        :return: None
        """
        if not event.is_directory:
            print(f"파일이 수정되었습니다: {event.src_path}")

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        """
        파일이 이동되었을 때 호출되는 메서드
        :param event: 파일/디렉터리 이동 이벤트
        :return: None
        """
        if not event.is_directory:
            print(f"파일이 이동되었습니다: {event.src_path} -> {event.dest_path}")
