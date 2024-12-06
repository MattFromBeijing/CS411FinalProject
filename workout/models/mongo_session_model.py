import logging
from typing import Any, List

from workout.clients.mongo_client import sessions_collection
from workout.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


def login_user(user_id: int) -> None:
    """
    Load the user's combatants from MongoDB into the BattleModel's combatants list.

    Checks if a session document exists for the given `user_id` in MongoDB.
    If it exists, clears any current combatants in `battle_model` and loads
    the stored combatants from MongoDB into `battle_model`.

    If no session is found, it creates a new session document for the user
    with an empty combatants list in MongoDB.

    Args:
        user_id (int): The ID of the user whose session is to be loaded.
    """
    logger.info("Attempting to log in user with ID %d.", user_id)
    session = sessions_collection.find_one({"user_id": user_id})

    if session:
        logger.info("Session found for user ID %d.")
    else:
        logger.info("No session found for user ID %d.", user_id)
        sessions_collection.insert_one({"user_id": user_id})
        logger.info("New session created for user ID %d.", user_id)
"""    
def logout_user(user_id: int) -> None:
    
    This does absolutely nothing right now because nothing is stored with the users

    Args:
        user_id (int): The ID of the user whose session data is to be saved.

    Raises:
        ValueError: If no session document is found for the user in MongoDB.
    
    logger.info("Attempting to log out user with ID %d.", user_id)
    logger.debug("Current combatants for user ID %d: %s", user_id)

    result = sessions_collection.update_one(
        {"user_id": user_id},
        upsert=False  # Prevents creating a new document if not found
    )

    if result.matched_count == 0:
        logger.error("No session found for user ID %d. Logout failed.", user_id)
        raise ValueError(f"User with ID {user_id} not found for logout.")

    logger.info("No data successfully saved for user ID %d.", user_id)
    logger.info("Nothing cleared for user ID %d.", user_id)
"""
    