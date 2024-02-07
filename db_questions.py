from sqlalchemy import create_engine, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional


class Base(DeclarativeBase):
    pass


class Question(Base):
    __tablename__ = "questions_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(20))
    correct_answer: Mapped[Optional[str]] = mapped_column(String(20))

    variants_answers: Mapped[List["Answers"]] = relationship(
        back_populates="question", cascade="all, delete-orphan"
    )

    def __str__(self) -> str:
        return f"{self.id} {self.question} {self.correct_answer} {self.variants_answers}"

    def __repr__(self) -> str:
        return f"{self.id} {self.question} {self.correct_answer} {self.variants_answers}"


class Answers(Base):
    __tablename__ = "answers_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[Optional[str]] = mapped_column(String(20))

    question: Mapped["Question"] = relationship(back_populates="variants_answers")
    question_id: Mapped[int] = mapped_column(ForeignKey("questions_table.id"))

    def __str__(self) -> str:
        return f"{self.id} {self.answer}"

    def __repr__(self) -> str:
        return f"{self.id} {self.answer}"


engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)
