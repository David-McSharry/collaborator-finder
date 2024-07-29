from scraper import get_user_summaries_by_tag
import asyncio

result = asyncio.run(get_user_summaries_by_tag("deceptive-alignment"))

# output is a list of dictionaries, format the json nicely and write to a file

import json

with open("tags_output.json", "w") as f:
    json.dump(result, f, indent=4)