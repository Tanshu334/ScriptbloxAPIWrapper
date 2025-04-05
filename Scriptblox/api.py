import requests
import inspect
from typing import Literal

class ScriptbloxAPI:
    def __init__(self, base_url="https://scriptblox.com/api"):
        self.base_url = base_url

    def _snake_to_camel(snake_str):
        parts = snake_str.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])
    
    def _bool_to_binary(value):
        return 1 if value else 0

    async def fetch_scripts(self, page: int = 1, max: int = 20, exclude: str = None, mode: Literal["free", "paid"] = None, patched: bool = None, key: bool = None, universal: bool = None, verified: bool = None, sort_by: Literal["views", "likeCount", "createdAt", "updatedAt", "dislikeCount"] = "updatedAt", order: Literal["asc", "desc"] = "desc"):
        """
        Fetches scripts from the Scriptblox API.
        Args:
            page (int): The page to start fetching from (useful for paginating content)
            max (int): Maximum amount of scripts to fetch in a batch (must be <= 20)
            exclude (str): Mainly internal, used to exclude a certain script from the results.
            mode (str): The script type
                - "free": Free scripts
                - "paid": Paid scripts
            patched (bool): Whether or not the script is patched
            key (bool): Whether or not the script has a key system
            universal (bool): Whether or not the script is universal
            verified (bool): Whether or not the script is verified
            sort_by (str): Used to control the criteria by which to sort the results
                - "views": Sort by views
                - "likeCount": Sort by like count
                - "createdAt": Sort by creation date
                - "updatedAt": Sort by last updated date
                - "dislikeCount": Sort by dislike count
            order (str): The sort order
                - "asc": Ascending order
                - "desc": Descending order
        Returns:
            - A list of scripts matching the specified criteria
        Raises:
            - ValueError: If the `max` parameter is greater than 20
        """
        if max > 20:
            raise ValueError("The `max` parameter must be less than or equal to 20.")
        
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        
        query_list = []
        query_string = "?"

        for arg in args:
            if arg == "self":
                continue

            value = values[arg]
            if value is not None:
                if isinstance(value, bool):
                    value = self._bool_to_binary(value)

                query_list.append(f"{self._snake_to_camel(arg)}={value}")

        query_string += "&".join(query_list)
        url = f"{self.base_url}/script/fetch{query_string}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["result"]["scripts"]