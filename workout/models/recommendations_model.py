import logging
import os

from exercises_model import Exercise

from workout.db import db
from workout.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class RecommendationsModel:
    """
    A class to manage recommending exercises to the user

    Attributes:
        target_groups (List[int]): muscle groups the user wants to focus on
        exercises (List[string]): a corresponding exercise for each muscle group
    """

    def __init__(self):
        """
        Initializes the ExercisesModel with an empty target_groups and empty exercises
        """
        self.target_groups: []
        self.exercises = []