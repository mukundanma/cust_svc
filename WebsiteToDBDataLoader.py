import os
import configparser
from dotenv import load_dotenv
from openai import OpenAI

from DBClient import DBClient
from crawler.WebScraper import WebScraper
from splitter.Splitter import Splitter
from Vectorizer import Vectorizer

# 1. Crawl the website and save documents
# 2. For each document in folder
#    a. Split into chunks
#    b. Vectorise the chunk
#    c. Save to DB
# 3. Choose LLM - langchain
# 4. Create Workflow
# 5. Create Streamlit UI
# 6. Answer Questions

load_dotenv()

config = configparser.ConfigParser()
config.read("config.properties")

client = OpenAI()

# scraper = WebScraper()
# scraper.crawl_website(website_url, download_folder, error_directory, company_name)

download_folder = config["APP"]["download_folder"]
error_directory = config["APP"]["error_directory"]
data_directory = config["APP"]["data_directory"]

website_url = config["CLIENT"]["website_url"]
company_name = config["CLIENT"]["company_name"]
subject = config["CLIENT"]["subject"]

db_type = config["DATABASE"]["db_type"]
uri = config["DATABASE"]["uri"]
db_name = config["DATABASE"]["db_name"]
collection_name = config["DATABASE"]["collection_name"]

model = config["MODEL"]["model"]
dimensions = int(config["MODEL"]["dimensions"])

data_path = os.path.join(data_directory, company_name)
if not os.path.exists(data_path):
    raise ("data directory doesn't exist")

splitter = Splitter()
vectorizer = Vectorizer(client, model, dimensions)
db_client = DBClient(db_type, uri, db_name)

chunk_count = 0


def insert_data_to_db(chunks):
    vectors = vectorizer.vectorize(chunks)
    print(len(vectors))
    # print(type(vectors))
    # data = {
    #     "id": chunk_count,
    #     "vector": vectors,
    #     "text": chunk,
    #     "subject": subject,
    # }
    data = [
        {"id": i, "vector": vectors[i], "text": chunks[i], "subject": subject}
        for i in range(len(chunks))
    ]
    print(data)
    # data = []
    # for i in range(len(vectors)):
    #     if i == 512:
    #         print("data: ", data)
    #         db_client.insert(collection_name, data)
    #         data = []
    #     data.append(
    #         {"id": i, "vector": vectors[i], "text": chunks[i], "subject": subject}
    #     )

    # if len(data) > 0:
    #     print("data: ", data)
    db_client.insert(collection_name, data)


def process_file(file_path):
    global chunk_count
    with open(file_path, "r", encoding="utf-8") as file:
        # content = file.read()

        docs = [
            "Artificial intelligence was founded as an academic discipline in 1956.",
            "Alan Turing was the first person to conduct substantial research in AI.",
            "Born in Maida Vale, London, Turing was raised in southern England.",
        ]

        # Split into chunks
        chunks = []
        for doc in docs:
            chunk = splitter.get_text_chunks(doc)
            print("chunk: ", chunk)
            chunks.extend(chunk)

        print(chunks)
        # Vectorise the chunk
        chunk_count += 1
        insert_data_to_db(chunks)


def process_all_files():
    for doc in os.listdir(data_path):
        print(
            "************* processing ***********",
            doc,
            "*********************",
        )
        file_path = os.path.join(data_path, doc)

        process_file(file_path)
        break


process_all_files()
