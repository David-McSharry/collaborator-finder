from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from scraper import get_user_summaries_by_tag
# from find_friends import find_a_friend
import json
from final_processing import find_a_friend
from openai import OpenAI
import os
app = FastAPI()


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserProfile(BaseModel):
    tag: str
    user_profile: str

@app.post("/recommend_friends")
async def recommend_friends(request: UserProfile):
    try:
        # Get user summaries by tag
        potential_friends_and_their_work = await find_a_friend(request.tag, request.user_profile)

        with OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) as client:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": potential_friends_and_their_work},
                    {"role": "user", "content": "Find friends for me"}
                ],
                max_tokens=1000
            )

        recommended_friends = response.choices[0].message.content.strip()

        return {"recommended_friends": recommended_friends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))