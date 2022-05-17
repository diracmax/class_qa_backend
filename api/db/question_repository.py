from interface.repository_interface import QuestionRepositoryInterface
from data.question_data import QuestionData


class QuestionRepository(QuestionRepositoryInterface):
    def __init__(self, connection):
        self.conn = connection

    def get_all_questions_by(self, class_id: int):
        # DBクライアントを作成する
        cursor = self.conn.cursor()

        query = "SELECT * FROM QUESTIONS WHERE class_id = %s"
        cursor.execute(query, [class_id])
        question_queries = cursor.fetchall()
        question_objects = []
        for query in question_queries:
            question_object = QuestionData(
                id=query[0],
                class_id=query[1],
                user_id=query[2],
                content=query[3],
                created_at=query[4]
            )
            question_objects.append(question_object)
        return question_objects
