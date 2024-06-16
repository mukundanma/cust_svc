import os
import configparser
from dotenv import load_dotenv
from openai import OpenAI

from DBClient import DBClient
from crawler.WebScraper import WebScraper
from splitter.Splitter import Splitter
from Vectorizer import Vectorizer

# 1. Choose LLM - langchain
# 2. Create Workflow
# 3. Create Streamlit UI
# 4. Answer Questions

load_dotenv()

config = configparser.ConfigParser()
config.read("config.properties")

client = OpenAI()

website_url = config["CLIENT"]["website_url"]
company_name = config["CLIENT"]["company_name"]
subject = config["CLIENT"]["subject"]

db_type = config["DATABASE"]["db_type"]
uri = config["DATABASE"]["uri"]
db_name = config["DATABASE"]["db_name"]
collection_name = config["DATABASE"]["collection_name"]

model = config["MODEL"]["model"]
dimensions = int(config["MODEL"]["dimensions"])

db_client = DBClient(db_type, uri, db_name)

# def query_message(
#     query: str,
#     model: str,
#     token_budget: int
# ) -> str:
#     introduction = 'Use the below articles to answer the subsequent question. If the answer cannot be found in the articles, write "I could not find an answer."'
#     question = f"\n\nQuestion: {query}"
#     message = introduction
#     for string in strings:
#         next_article = f'\n\nWikipedia article section:\n"""\n{string}\n"""'
#         if (
#             num_tokens(message + next_article + question, model=model)
#             > token_budget
#         ):
#             break
#         else:
#             message += next_article
#     return message + question

# input_text = input("Please enter your search term: ")

# vectorizer = Vectorizer(client, model, dimensions)

# query_vectors = list(vectorizer.vectorize(input_text))

queries = ["What is the wheelbase of Alto K 10?"]

query_vectors = [
    vec.embedding
    for vec in client.embeddings.create(
        input=queries, model=model, dimensions=dimensions
    ).data
]

query_resp = db_client.searchDB(collection_name, query_vectors)

print(query_resp)
