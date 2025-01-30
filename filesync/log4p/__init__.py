"""
로그 관련 처리를 일관성 있게 하기 위한 로깅 모듈
"""
import logging

from logging import Logger


class Log(object):
    """
    로깅 클래스
    """

    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter("[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s")

        # 콘솔 로그 출력 핸들러
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # 파일 로그 기록 핸들러
        file_handler = logging.FileHandler("filesync.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    @property
    def get_logger(self) -> Logger:
        return self.logger
