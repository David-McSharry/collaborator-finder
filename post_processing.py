import subprocess
import sys
from bs4 import BeautifulSoup
import os
from openai import OpenAI
import json
import aiohttp
from openai import AsyncOpenAI
import asyncio


# async def process_and_summarize_post(url: str) -> str:
#     """
#     Takes in a single url, parses the post content, and summarizes it.
#     """
#     assert url.startswith('https://www.greaterwrong.com/posts'), f"Invalid URL >>{url}<< Please provide a valid LessWrong post URL."
    
#     async def summarize_post(text: str) -> str:
#         client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
#         try:
#             with open('prompts/post_summarizer.txt', 'r') as file:
#                 post_summarizer_content = file.read()

#             response = await client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=[
#                     {"role": "system", "content": post_summarizer_content},
#                     {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
#                 ],
#                 max_tokens=1000
#             )
            
#             return response.choices[0].message.content.strip()
#         except Exception as e:
#             return f"An error occurred while summarizing: {str(e)}"
        

#     main_text = await extract_main_text_in_post(url)
#     if not main_text.startswith("Failed") and not main_text.startswith("An error occurred"):
#         return await summarize_post(main_text)
#     else:
#         return main_text  # Return the error message if extraction failed



async def extract_main_text_in_post(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find the main content
        main_content = soup.find('div', class_='post-body')
        
        if main_content:
            # Extract text from all paragraphs
            paragraphs = main_content.find_all('p')
            main_text = ' '.join([p.get_text().strip() for p in paragraphs])
            return main_text
        else:
            return "Main content not found. The page structure might have changed."
    
    except aiohttp.ClientError as e:
        return f"Failed to fetch the content from {url}: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


async def extract_user_posts(username: str) -> list[dict]:
    """
    Takes in a username, fetches the last 5 posts by the user, and summarizes them.
    """
    try:
        # Construct the URL for the user's posts
        url = f"https://www.greaterwrong.com/users/{username}?show=posts"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
        
        # Parse the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find all post elements
        post_elements = soup.find_all('h1', class_='listing')
        
        # Prepare tasks for concurrent execution
        links = []
        tasks = []
        for post in post_elements:
            title_link = post.find('a', class_='post-title-link')
            if title_link:
                title = title_link.get_text().strip()
                link = "https://www.greaterwrong.com" + title_link['href']
                # tasks.append(asyncio.create_task(process_and_summarize_post(link)))
                links.append(link)


        tasks = [asyncio.create_task(extract_main_text_in_post(link)) for link in links]
        texts = await asyncio.gather(*tasks)

        # Create a JSON of links and texts
        result = [{"link": link, "text": text} for link, text in zip(links, texts)]

        return result
    
    except aiohttp.ClientError as e:
        return f"Failed to fetch the webpage: {str(e)}"
    except Exception as e:
        return f"An error occurred while processing posts: {str(e)}"
    

# result = asyncio.run(get_user_posts_summarized("jozdien"))

# print(result)
    #     tasks = tasks[:5]  # Limit to 5 posts
        
    #     # Execute all tasks concurrently
    #     summarized_posts = await asyncio.gather(*tasks)
        
    #     # Combine title and summary
    #     result = []
    #     for post, summary in zip(post_elements[:5], summarized_posts):
    #         title_link = post.find('a', class_='post-title-link')
    #         if title_link:
    #             title = title_link.get_text().strip()
    #             result.append({
    #                 'title': title,
    #                 'link': "https://www.greaterwrong.com" + title_link['href'],
    #                 'summary': summary
    #             })
        
    #     return result
    
    # except aiohttp.ClientError as e:
    #     return f"Failed to fetch the webpage: {str(e)}"
    # except Exception as e:
    #     return f"An error occurred while processing posts: {str(e)}"
