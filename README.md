To spin up backend API, add `OPENAI_API_KEY` to environment variables, install requirements and run:

`
uvicorn app:app --reload
`

To spin up frontend run:

`
streamlit run frontend.py
`

The depth of LLM search is currently quite shallow due to inference cost + rate limits from greaterwrong.com, but can pretty easily scaled up at a later date. To produce better outputs you can probably replace hardcoded gpt-4o-mini with gpt-4o.
