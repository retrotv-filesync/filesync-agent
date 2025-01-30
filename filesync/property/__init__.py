"""
프로퍼티 관련 처리를 일관성 있게 하기 위한 프로퍼티 모듈
"""
import configparser
from configparser import SectionProxy


class Property(object):
    """
    프로퍼티 클래스
    """

    def __init__(self, filename: str, property_name: str) -> None:
        properties = configparser.ConfigParser()
        properties.read(filename)
        self.properties = properties[property_name]

    @property
    def get_properties(self) -> SectionProxy:
        return self.properties
