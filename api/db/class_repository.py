from interface.repository_interface import ClassRepositoryInterface
from data.class_data import ClassData


class ClassRepository(ClassRepositoryInterface):
    def __init__(self, connection):
        self.conn = connection

    def get_all_classes(self):
        # DBクライアントを作成する
        cursor = self.conn.cursor()

        query = "SELECT * FROM CLASSES"
        cursor.execute(query)
        class_queries = cursor.fetchall()
        class_objects = []
        for query in class_queries:
            class_object = ClassData(
                id=query[0],
                name=query[1],
                semester=query[2],
                year=query[3]
            )
            class_objects.append(class_object)
        return class_objects
