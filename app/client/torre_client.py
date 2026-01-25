import httpx
from app.core.constants import BASE_GENOME_URL, BASE_OPPORTUNITIES_URL


class TorreClient:
    def __init__(self):
        self.client = httpx.AsyncClient()

    async def get_user_genome(self, username: str) -> dict:
        """
        Retrieves the genomic data of a specified user asynchronously.

        This function fetches and returns the genome information associated with
        the provided username. The genomic data is provided in dictionary format.

        :param username: The username whose genomic data is to be retrieved.
        :return: A dictionary containing the genomic data for the specified user.
        """
        resp = await self.client.get(f"{BASE_GENOME_URL}/{username}")
        resp.raise_for_status()
        return resp.json()

    async def find_opportunities(self, skill: str, limit: int = 10) -> dict:
        """
        Finds and retrieves opportunities related to a specific skill.

        This method performs an asynchronous operation to search for opportunities
        that match the given skill. The number of results returned can be limited
        by providing the `limit` parameter. Results are returned as a dictionary
        containing the relevant information.

        :param skill: A string representing the skill to search for opportunities.
        :param limit: An integer specifying the maximum number of results to retrieve.
            Defaults to 10.
        :return: A dictionary containing the retrieved opportunities.
        """
        body = {
            "and":
                [
                    {"skill/role":
                        {
                            "text": skill,
                            "proficiency": "expert"
                        }
                    },
                    {
                        "status":
                            {
                                "code": "open"
                            }
                    }
                ]
        }

        resp = await self.client.post(f"{BASE_OPPORTUNITIES_URL}?size={limit}", json=body)
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()
