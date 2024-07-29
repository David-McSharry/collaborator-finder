from scraper import get_user_summaries_by_tag
import asyncio
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def find_a_friend(
    potential_friends: str, # a str rep of a json list of potential friends
    personal_profile: str # a str rep of ones interests
) -> str: # a str rep of a json list of potential friends
    
    with open("prompts/find_a_friend.txt", "r") as f:
        prompt = f.read()

    prompt = prompt.replace("{{forum_users}}", potential_friends)
    prompt = prompt.replace("{{user_profile}}", personal_profile)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Find friends for me"}
        ],
        max_tokens=1000
    )

    return response.choices[0].message.content.strip()

# user_profile = "I am interested in the relationship between mesa-ootimisation and deceptive alignment"

# with open("tags_output.json", "r") as f:
#     potential_friends = f.read()

# result = find_a_friend(potential_friends, user_profile)

# print(result)


