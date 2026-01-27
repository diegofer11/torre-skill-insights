from app.client.torre_client import TorreClient
from app.core.validators import validate_username


async def get_user_skills_service(username: str) -> dict:
    """
    Asynchronously retrieves a user's skills based on their genome data.

    This function interacts with the `TorreClient` service to fetch the user's
    genome data, extracts the strengths from it, and compiles a list of skills.
    The function ensures proper cleanup of the client connection upon completion.

    :param username: The username of the user whose skills are to be retrieved.
    :return: A dictionary containing the username and their extracted skills.
    """
    validate_username(username)
    client = TorreClient()
    try:
        genome = await client.get_user_genome(username)
        strengths = genome.get("strengths", [])
        skills = [s.get("name") for s in strengths if "name" in s]
    finally:
        await client.close()

    return {"username": username, "skills": skills}
