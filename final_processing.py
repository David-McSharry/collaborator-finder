from comment_processing import extract_profile_comments
from post_processing import extract_user_posts
from scraper import get_users_from_a_tag
import json

import asyncio
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def find_a_friend(
    tag: str, 
    personal_profile: str # a str rep of ones interests
) -> str: # a str rep of a json list of potential friends
    
    potential_friends = await get_users_from_a_tag(tag)

    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print(potential_friends)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    potential_friends = potential_friends[:3]

    # for each user in potential_friends, get their comments and posts
    users_and_posts_and_comments = {}
    for user in potential_friends:
        comments = await (extract_profile_comments(user))
        posts = await (extract_user_posts(user))
        users_and_posts_and_comments[user] = {
            user: {
                # "comments": comments,
                "posts": posts[:4]
            }
        }

    potential_friends = json.dumps(users_and_posts_and_comments, indent=4)

    with open("prompts/find_a_friend.txt", "r") as f:
        prompt = f.read()

    prompt = prompt.replace("{{forum_users}}", potential_friends)
    prompt = prompt.replace("{{user_profile}}", personal_profile)
    print('-------------------------------------------')
    print(prompt)
    print('-------------------------------------------')
    return prompt
# tag = "deceptive-alignment"
# user_profile = "I am interested in the relationship between mesa-ootimisation and deceptive alignment"

# result = find_a_friend(tag, user_profile)