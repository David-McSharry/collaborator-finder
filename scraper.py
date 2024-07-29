import subprocess
import sys
from bs4 import BeautifulSoup
import os
from openai import OpenAI
import json
import aiohttp
from openai import AsyncOpenAI
import asyncio
from comment_processing import process_and_summarize_comments
# from post_processing import get_user_posts_summarized


async def get_users_from_a_tag(tag: str) -> list[str]:
    # This function takes a tag as a string and returns a list of users from the first 4 posts

    url = f"https://www.greaterwrong.com/tag/{tag}?sort=new"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        
        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all post sections
        posts = soup.find_all('div', class_='post-meta')[3:5]  # Limit to the first 4 posts
        
        # Set to store unique users
        users = []
        
        for post in posts:
            # Find all authors for this post
            authors = post.find_all('a', class_='author')
            
            for author in authors:
                username = author['href'].split('/')[-1]
                if username not in users:
                    users.append(username)
        
        return users        
    except aiohttp.ClientError as e:
        raise Exception(f"Failed to fetch the webpage: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred while processing posts: {str(e)}")

async def get_user_summaries_by_tag(tag: str) -> dict[str, list[dict]]:
    # Get relevant users for the tag
    print(f"Getting user summaries for tag: >>>{tag}<<<")
    users_array = await get_users_from_a_tag(tag)

    print(f"Users array: {users_array}")
    
    async def get_user_summary(username: str) -> dict:
        comments_summary = await process_and_summarize_comments(username)
        posts_summary = await get_user_posts_summarized(username)
        return {
            'username': username,
            'comments_summary': comments_summary,
            'posts_summary': posts_summary
        }
    
    tasks = [asyncio.create_task(get_user_summary(user)) for user in users_array]
    user_summaries = await asyncio.gather(*tasks)

    print(f"Got user summaries for tag: {tag}")
    with open("frontend_user_summaries.json", "w") as f:
        f.write(json.dumps(user_summaries, indent=4))
    
    return user_summaries
