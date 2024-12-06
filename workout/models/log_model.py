from dataclasses import dataclass
import logging
import os

from sqlalchemy.exc import IntegrityError

from user_model import Users
from exercise_model import Exercise

from workout.db import db
from workout.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class Log:
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    muscle_group = Column(Integer, nullable=False)
    date = Column(String, nullable=False)

def create_log(userId: int, exercise: Exercise) -> None:
    if len(exercise.name) < 0:
        raise ValueError(f"Invalid exercise name provided: {name} (must be an string with length greater than 0).")

    try:
        new_log = Log(user_id=userId, name=exercise.name, muscle_group=exercise.muscle_group, date=exercise.date)
        db.session.add(new_log)
        db.session.commit()
        logger.info("Log successfully added to the database")
    except Exception as e:
        db.session.rollback()
        logger.error("Database error: %s", str(e))
        raise