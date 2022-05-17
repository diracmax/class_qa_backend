from abc import abstractmethod, ABCMeta

from data.user_data import UserData


class UserRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def get(self, username: str) -> UserData:
        pass

    @abstractmethod
    def save(self, username: str, password: str) -> bool:
        pass

    @abstractmethod
    def exist(self, username: str) -> bool:
        pass


class ClassRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_all_classes(self):
        pass


class QuestionRepositoryInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_all_questions_by(self, class_id: int):
        pass
