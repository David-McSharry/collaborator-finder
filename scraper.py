import subprocess
import sys
from bs4 import BeautifulSoup
import os
from openai import OpenAI
import json
import aiohttp
from openai import AsyncOpenAI
import asyncio

# def extract_profile_comments(url: str):
#     try:
#         assert url.startswith('https://www.greaterwrong.com/users'), "Invalid URL. Please provide a valid GreaterWrong user profile URL."
#         assert url.endswith('?show=comments'), "Invalid URL. Please provide a valid GreaterWrong user profile comments URL."
#         # Use curl to fetch the webpage content
#         result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, check=True)
        
#         # Parse the HTML content
#         soup = BeautifulSoup(result.stdout, 'html.parser')
        
#         # Find all comment elements
#         comment_elements = soup.find_all('li', class_='comment-item')

#         comments = []
#         for comment in comment_elements:
#             author = comment.find('a', class_='author').get_text().strip()
#             text = comment.find('div', class_='comment-body').get_text().strip()
#             date = comment.find('a', class_='date').get_text().strip()
#             karma = comment.find('span', class_='karma-value').get_text().strip().split()[0]
#             post_title = comment.find('span', class_='comment-post-title2').find('a').get_text().strip()
#             comment_link = comment.find('a', class_='permalink')['href']
            
#             comments.append({
#                 'author': author,
#                 'text': text,
#                 'date': date,
#                 'karma': karma,
#                 'post_title': post_title,
#                 'comment_link': f"https://www.greaterwrong.com{comment_link}"
#             })
        
#         return comments
    
#     except subprocess.CalledProcessError as e:
#         return f"Failed to fetch the webpage: {str(e)}"
#     except Exception as e:
#         return f"An error occurred while extracting comments: {str(e)}"
    
# NOTE: we will only use async version
# def process_and_summarize_comments(url: str):
#     assert url.startswith('https://www.greaterwrong.com/users'), "Invalid URL. Please provide a valid GreaterWrong user profile URL."
#     assert url.endswith('?show=comments'), "Invalid URL. Please provide a valid GreaterWrong user profile comments URL."

#     def extract_profile_comments(url: str):
#         try:
#             assert url.startswith('https://www.greaterwrong.com/users'), "Invalid URL. Please provide a valid GreaterWrong user profile URL."
#             assert url.endswith('?show=comments'), "Invalid URL. Please provide a valid GreaterWrong user profile comments URL."
#             # Use curl to fetch the webpage content
#             result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, check=True)
            
#             # Parse the HTML content
#             soup = BeautifulSoup(result.stdout, 'html.parser')
            
#             # Find all comment elements
#             comment_elements = soup.find_all('li', class_='comment-item')
            
#             comments = []
#             for comment in comment_elements:
#                 author = comment.find('a', class_='author').get_text().strip()
#                 text = comment.find('div', class_='comment-body').get_text().strip()
#                 date = comment.find('a', class_='date').get_text().strip()
#                 karma = comment.find('span', class_='karma-value').get_text().strip().split()[0]
#                 post_title = comment.find('span', class_='comment-post-title2').find('a').get_text().strip()
#                 comment_link = comment.find('a', class_='permalink')['href']
                
#                 comments.append({
#                     'author': author,
#                     'text': text,
#                     'date': date,
#                     'karma': karma,
#                     'post_title': post_title,
#                     'comment_link': f"https://www.greaterwrong.com{comment_link}"
#                 })
            
#             return comments
        
#         except subprocess.CalledProcessError as e:
#             return f"Failed to fetch the webpage: {str(e)}"
#         except Exception as e:
#             return f"An error occurred while extracting comments: {str(e)}"

    
#     def summarize_comments(text):
#         client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
#         try:
#             with open('prompts/comment_summarizer.txt', 'r') as file:
#                 comment_summarizer_content = file.read()

#             response = client.chat.completions.create(
#                 model="gpt-4o-mini",
#                 messages=[
#                     {"role": "system", "content": comment_summarizer_content},
#                     {"role": "user", "content": f"Please summarize the following user comments:\n\n{text}"}
#                 ],
#                 max_tokens=1000
#             )
            
#             return response.choices[0].message.content.strip()
#         except Exception as e:
#             return f"An error occurred while summarizing: {str(e)}"
    
#     comments = extract_profile_comments(url)
#     if isinstance(comments, list) and comments:
#         concatenated_comments = "\n----\n".join([comment['text'] for comment in comments])
#         return summarize_comments(concatenated_comments)
#     else:
#         return comments  # Return the error message if extraction failed





# def process_and_summarize_post(url):
#     assert url.startswith('https://www.greaterwrong.com/posts'), "Invalid URL. Please provide a valid LessWrong post URL."
    
#     def summarize_post(text):
#         client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
#         try:
#             with open('prompts/post_summarizer.txt', 'r') as file:
#                 post_summarizer_content = file.read()

#             response = client.chat.completions.create(
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
        
#     def extract_main_text_in_post(url):
#         try:
#             # Use curl to fetch the webpage content
#             result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, check=True)
            
#             # Parse the HTML content
#             soup = BeautifulSoup(result.stdout, 'html.parser')
            
#             # Find the main content
#             main_content = soup.find('div', class_='post-body')
            
#             if main_content:
#                 # Extract text from all paragraphs
#                 paragraphs = main_content.find_all('p')
#                 main_text = ' '.join([p.get_text().strip() for p in paragraphs])
#                 return main_text
#             else:
#                 return "Main content not found. The page structure might have changed."
        
#         except subprocess.CalledProcessError:
#             return f"Failed to fetch the content from {url}"
#         except Exception as e:
#             return f"An error occurred: {str(e)}"


#     main_text = extract_main_text_in_post(url)
#     if not main_text.startswith("Failed") and not main_text.startswith("An error occurred"):
#         return summarize_post(main_text)
#     else:
#         return main_text  # Return the error message if extraction failed



def get_relevant_users_in_tag(tag):
    # This function takes a tag as a string and returns a JSON with users and their posts

    url = f"https://www.greaterwrong.com/tag/{tag}"
    
    try:
        # Use curl to fetch the webpage content
        result = subprocess.run(['curl', '-s', url], capture_output=True, text=True, check=True)
        
        # Parse the HTML content
        soup = BeautifulSoup(result.stdout, 'html.parser')
        
        # Find all post sections
        posts = soup.find_all('div', class_='post-meta')
        
        # Dictionary to store users and their associated links
        user_links = {}
        
        for post in posts:
            # Find the post link
            listing = post.find_previous('h1', class_='listing')
            if listing:
                post_link_elem = listing.find('a', class_='post-title-link')
                if post_link_elem and 'href' in post_link_elem.attrs:
                    post_link = post_link_elem['href']
                    full_post_link = f"https://www.greaterwrong.com{post_link}"
                    
                    # Find all authors for this post
                    authors = post.find_all('a', class_='author')
                    
                    for author in authors:
                        username = author.text.strip()
                        if username not in user_links:
                            user_links[username] = []
                        user_links[username].append(full_post_link)
        
        # Convert set to list for JSON serialization
        for user in user_links:
            user_links[user] = list(set(user_links[user]))
        
        return json.dumps(user_links)
        
    except subprocess.CalledProcessError as e:
        return json.dumps({"error": f"Error occurred while fetching the webpage: {str(e)}"})
    except Exception as e:
        return json.dumps({"error": f"An unexpected error occurred: {str(e)}"})
    


    

async def process_user(username):
    # Convert username to lowercase and replace spaces with dashes
    formatted_username = username.lower().replace(' ', '-')
    
    # Get and summarize user's comments
    print(f"username about to be processed: {formatted_username}")
    comments_summary = await process_and_summarize_comments(username=formatted_username)

    i = 0
    if comments_summary is []:
        # try again in i seconds
        i += 1
        await asyncio.sleep(i)
        comments_summary = await process_and_summarize_comments(username=formatted_username)
        if i > 10:
            print(f"Failed to get comments for {formatted_username}")
            return formatted_username, (comments_summary, None)


    print('comments acquired')
    # Get and summarize user's posts
    posts_summary = await get_user_posts_summarized(formatted_username)
    print('posts acquired')

    print(f"first part of comments_summary for {formatted_username}: {str(comments_summary[:100])}")
    print(f"first part of posts_summary for {formatted_username}: {str(posts_summary[:100])}")

    return formatted_username, (comments_summary, posts_summary)

async def get_user_summaries_by_tag(tag: str):
    # Get relevant users for the tag
    users_json = get_relevant_users_in_tag(tag)
    users_dict = json.loads(users_json)


    for username in users_dict:
        print(f"Processing user: {username}")
    
    # Process all users concurrently
    tasks = [process_user(username) for username in users_dict]
    results = await asyncio.gather(*tasks)

    # Convert results to dictionary
    result_dict = dict(results)

    return json.dumps(result_dict)
