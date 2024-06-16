import json
from pymilvus import MilvusClient


class DBClient:
    def __init__(self, type, uri, db_name):
        if type == "Milvus":
            self._client = MilvusClient(uri=uri, db_name=db_name)
        else:
            raise ("Invalid db type")

    def insert(self, collection_name, data):
        res = self._client.insert(collection_name, data=data)
        print("inserted data into db", res)

    def searchDB(self, collection_name, query_vectors):
        search_results = self._client.search(
            collection_name=collection_name,
            data=query_vectors,
            output_fields=["text", "subject"],
            limit=5,
        )

        result = json.dumps(search_results, indent=4)
        return result
