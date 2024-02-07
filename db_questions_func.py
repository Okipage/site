from __future__ import annotations
from sqlalchemy.orm import Session
from db_questions import engine, Question, Answers

session = Session(engine)


def show_db():
    questions = session.query(Question).all()
    for question in questions:
        print(question)


def get_questions() -> list[dict[str | list[str]]]:
    questions = session.query(Question).all()
    variants_answers = [[answer.answer for answer in question.variants_answers]
                        for question in questions]

    return [{"question": question.question,
             "variants": variants_answers[ind],
             "correct_answer": question.correct_answer}
            for ind, question in enumerate(questions)]


def add_question(question: str, variants_answers: list[str], correct_answer: str):
    with session.begin():
        session.add(Question(
            question=question,
            variants_answers=[Answers(answer=answer) for answer in variants_answers],
            correct_answer=correct_answer)
        )


def get_correct_answers() -> list[str]:
    questions = get_questions()
    return [question["correct_answer"] for question in questions]


if __name__ == "__main__":
    show_db()
