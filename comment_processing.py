import subprocess
import sys
from bs4 import BeautifulSoup
import os
from openai import OpenAI
import json
import aiohttp
from openai import AsyncOpenAI
import asyncio

async def process_and_summarize_comments(username: str) -> dict[str, str]:

    url = f"https://www.greaterwrong.com/users/{username}?show=comments"

    async def extract_profile_comments(url: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    content = await response.text()
            
            soup = BeautifulSoup(content, 'html.parser')
            comment_elements = soup.find_all('li', class_='comment-item')
            
            comments = []
            for comment in comment_elements:
                author = comment.find('a', class_='author').get_text().strip()
                text = comment.find('div', class_='comment-body').get_text().strip()
                date = comment.find('a', class_='date').get_text().strip()
                karma = comment.find('span', class_='karma-value').get_text().strip().split()[0]
                post_title = comment.find('span', class_='comment-post-title2').find('a').get_text().strip()
                comment_link = comment.find('a', class_='permalink')['href']
                
                comments.append({
                    'author': author,
                    'text': text,
                    'date': date,
                    'karma': karma,
                    'post_title': post_title,
                    'comment_link': f"https://www.greaterwrong.com{comment_link}"
                })
            
            return comments
        
        except aiohttp.ClientError as e:
            return f"Failed to fetch the webpage: {str(e)}"
        except Exception as e:
            return f"An error occurred while extracting comments: {str(e)}"

    async def summarize_comments(text):
        client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        try:
            with open('prompts/comment_summarizer.txt', 'r') as file:
                comment_summarizer_content = file.read()

            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": comment_summarizer_content},
                    {"role": "user", "content": f"Please summarize the following user comments:\n\n{text}"}
                ],
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"An error occurred while summarizing: {str(e)}"
    
    comments = await extract_profile_comments(url)
    if isinstance(comments, list) and comments:
        concatenated_comments = "\n----\n".join([comment['text'] for comment in comments])
        comment_summary = await summarize_comments(concatenated_comments)
        return {url: comment_summary}
    else:
        return comments  # Return the error message if extraction failed











async def extract_profile_comments(username: str):
    url = f"https://www.greaterwrong.com/users/{username}?show=comments"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        
        soup = BeautifulSoup(content, 'html.parser')
        comment_elements = soup.find_all('li', class_='comment-item')
        
        comments = []
        for comment in comment_elements:
            text = comment.find('div', class_='comment-body').get_text().strip()
            post_title = comment.find('span', class_='comment-post-title2').find('a').get_text().strip()
            
            comments.append({
                'text': text,
                'post_title': post_title,
            })
        
        return comments
    
    except aiohttp.ClientError as e:
        raise Exception(f"Failed to fetch the webpage: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred while extracting comments: {str(e)}")
    
# results = asyncio.run(extract_profile_comments("jozdien"))

# print(results[:5])

    
