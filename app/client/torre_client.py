import json

import httpx

from app.core.constants import BASE_GENOME_URL, BASE_OPPORTUNITIES_URL


class TorreClient:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=httpx.Timeout(20))

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

    async def find_opportunities(self, skills: list[str], limit: int = 5) -> dict:
        """
        Finds and retrieves opportunities related to a specific skill.

        This method performs an asynchronous operation to search for opportunities
        that match the given skill. The number of results returned can be limited
        by providing the `limit` parameter. Results are returned as a dictionary
        containing the relevant information.

        :param skills: A list of strings representing the skills to search for.
        :param limit: An integer specifying the maximum number of results to retrieve.
            Defaults to 10.
        :return: A dictionary containing the retrieved opportunities.
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.51.0"
        }

        body = {
            "or":
                [
                    *[
                        {
                            "skill/role":
                                {
                                    "text": skill,
                                    "proficiency": "expert"
                                }
                        }
                        for skill in skills
                    ],
                    {"status": {"code": "open"}}
                ]
        }
        print("Body enviado:", json.dumps(body, indent=2))

        resp = await self.client.post(f"{BASE_OPPORTUNITIES_URL}?size={limit}", json=body, headers=headers)

        print("Request URL:", resp.request.url)
        print("Request Headers:", resp.request.headers)
        print("Request Body:", resp.request.content.decode())

        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()
