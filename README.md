To spin up backend API, add `OPENAI_API_KEY` to environment variables, install requirements and run:

`
uvicorn app:app --reload
`

To spin up frontend run:

`
streamlit run frontend.py
`

The depth of LLM search is currently quite shallow due to inference cost + rate limits from greaterwrong.com, but can pretty easily scaled up at a later date. To produce better outputs you can probably replace hardcoded gpt-4o-mini with gpt-4o.

Demo can be viewed here:

https://www.loom.com/share/a587749cf4824f1cb5b216f9094dee37?sid=5d763d3b-0fa7-4df2-97b4-540dd2b7d235

<img width="444" alt="image" src="https://github.com/user-attachments/assets/6159edc4-8dfd-485a-91c7-54708fc4f312">
