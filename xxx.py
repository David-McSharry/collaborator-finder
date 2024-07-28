from comment_processing import process_and_summarize_comments
import asyncio

output = asyncio.run(process_and_summarize_comments("evhub"))

# output is a list of dictionaries, format the json nicely and write to a file

import json

with open("user_comments.json", "w") as f:
    json.dump(output, f, indent=4)