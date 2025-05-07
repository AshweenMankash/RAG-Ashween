A RAG Application with 3 main features: Authentication, Ingestion & Querying

There are 4 components in this project

1) API
2) Workers
3) Postgres
4) Redis

# API
This service uses fastapi and has 2 main endpoints Ingest and Query.

How ingestion works: You can pass in a file (Txt file or a PDF file) if you pass in a file with the same name it will remove all previous contents and renew it with this data.

How querying works: Given a question to the API it will generate embedding vector for the question search for the nearest cosine distance chunks and 
then pass it to chat-gpt to get a well formed response based on the context.

# Workers

a) Ingestion
It splits text data into chunks of size 500 characters It generates Embedding vector of size 384 and puts it into the database.

!! If the embedding vector size ever changes I would suggest dropping this column adding a new one and then regenerating embeddings.


b) querying
Passes your question to the model for embedding generator and then queries the database for nearest 5 embeddings.
Now that we have the context I pass it to openrouter.ai for Summary generation.

I have missed a few steps like question Decomposition since I am working at a startup and they are keeping me quite busy right now

## To get it quickly up and running
Assumptions:
    You have python3, docker installed and a proper network.

Open a terminal in the root diirectory of this project and run
    1) chmod +x setup.sh
    2) ./setup.sh (Assuming you have python installed)

We do this step to install the model on your local directory so that everytime you build the docker image it doesn't download the file again.
Since I am not using OpenAIEmbedding.

docker compose up --build

I am attaching a postman link to the requests.
https://bold-trinity-443557.postman.co/workspace/My-Workspace~b214d269-e6cc-44a5-883a-429afea6615b/collection/13664840-7d7cfaca-4fe9-444f-a0df-7ed20478f9c0?action=share&creator=13664840

also create an .env file in the root directory and insert

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=vector_db
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/vector_db
OPEN_ROUTER_API_KEY= <Visit Open Router and generate an API key and insert it here>
broker_url=redis://redis:6379/0
result_backend=redis://redis:6379/1
task_serializer=json
result_serializer=json
accept_content=json
SECRET_PASS_KEY="Your secret key, hope fully something strong"



I hope you like it!