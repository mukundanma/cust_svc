import json
from pymilvus import MilvusClient
from pymilvus import model
import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)


class DBUtil:

    def init(self, uri, db_name):
        self.client = MilvusClient(uri=uri, db_name=db_name)

        self.openai_ef = model.dense.OpenAIEmbeddingFunction(
            model_name="text-embedding-3-large",
            api_key=OPENAI_API_KEY,
            dimensions=512,
        )

    def createEmbeddingsForDocuments(self, docs, subject):
        vectors = self.openai_ef.encode_documents(docs)

        # Print dimension and shape of embeddings
        print("Dim:", self.openai_ef.dim, vectors[0].shape)

        data = [
            {"id": i, "vector": vectors[i], "text": docs[i], "subject": subject}
            for i in range(len(vectors))
        ]

        print("Data has", len(data), "entities, each with fields: ", data[0].keys())
        print("Vector dim:", len(data[0]["vector"]))
        return data

    def insertDataToDB(self, data):
        res = self.client.insert(collection_name="demo_collection", data=data)

        print("inserted data into db")
        print(res)

    # Single vector search
    def searchDB(self, queries):
        vectors = self.createQueryEmbeddings(queries=queries)

        search_results = self.client.search(
            collection_name="demo_collection",
            data=vectors,
            output_fields=["text", "subject"],
            limit=5,
            # search_params={"metric_type": "COSINE", "params": {}} # Search parameters
        )

        result = json.dumps(search_results, indent=4)
        return result

    def createQueryEmbeddings(self, queries):
        query_embeddings = self.openai_ef.encode_queries(queries)
        print("Dim", self.openai_ef.dim, query_embeddings[0].shape)
        return query_embeddings


dbUtil = DBUtil()

uri = "http://localhost:19530"
db_name = "demo_db"

dbUtil.init(uri=uri, db_name=db_name)

docs = [
    "Artificial intelligence was founded as an academic discipline in 1956.",
    "Alan Turing was the first person to conduct substantial research in AI.",
    "Born in Maida Vale, London, Turing was raised in southern England.",
]

# data = dbUtil.createEmbeddingsForDocuments(docs, "history")

# dbUtil.insertDataToDB(data=data)

queries = [
    "Alan Turing was the 1st person to perform quite a bit of research in Artificial Intelligence."
]

result = dbUtil.searchDB(queries=queries)

print("result: " + result)
