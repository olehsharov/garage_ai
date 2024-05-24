Prototype:

Local faiss vector db with local ingest.
Flask server that runs chatbot, pdf slicing, document retrival.
Rquires custom webui.

MVP:

Serverless app, that will only requires ingest to be executed on the server.

- Pipecone as vector db/search etc
- Google cloud python functions for processing
- Openai for chat api
- Streamlit for webui

Ingest (pinecone)
Ingest.py is a command line tool to slice pdfs to chunks and ingest data into pinecone.
Data ingested needs keep references to source pdfs and pages.
Data also needs to be uploaded to proper place to be then referenced.

- split (split pdf to pages)
- extract (extract text for each page)
- vectorize (save to pinecone)
- upload (upload to google cloud storage)

Retrieve (pinecone)
Retrieve.py is an utility to retrieve documents based on prompt

Generate
Generate.py is a utility that combines Retrieve and Chatgpt to make reply replacing 
references to links to certain pages of a pdf.

Streamlit_app
Streamlit_app.py is a simple chatbot ui with auth and pdf viewer.
