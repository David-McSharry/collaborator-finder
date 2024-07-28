from scraper import process_and_summarize_post
from scraper import process_and_summarize_comments
from scraper import get_user_posts_summarized
from scraper import get_user_summaries_by_tag
from scraper import process_user

import asyncio


# reuslt = asyncio.run(process_and_summarize_post("https://www.greaterwrong.com/posts/ZAsJv7xijKTfZkMtr/sleeper-agents-training-deceptive-llms-that-persist-through"))

# print(reuslt)

# result = asyncio.run(process_and_summarize_comments("https://www.greaterwrong.com/users/evhub?show=comments"))

# print(result)


# result = asyncio.run(process_user("Scott Garrabrant"))

# print(result)

result = asyncio.run(get_user_summaries_by_tag("deceptive-alignment"))

print(result)

# save the result to a file
with open("output.txt", "w") as f:
    f.write(result)