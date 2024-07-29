To spin up backend API install requirements and run:

`
uvicorn app:app --reload
`

To spin up frontend run:

`
streamlit run frontend.py
`

The depth of LLM search is currently quite shallow due to inference cost + rate limits from greaterwrong.com, but can pretty easily scaled up at a later date.
