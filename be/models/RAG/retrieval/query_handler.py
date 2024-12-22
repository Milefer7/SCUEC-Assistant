# be/retrieval/query_handler.py

import faiss
import numpy as np


class QueryHandler:
    def __init__(self, index: faiss.Index, documents: list):
        self.index = index  # 用于检索的索引
        self.documents = documents  # 文档库

    def retrieve(self, query: str, top_k: int = 5) -> list:
        # 将查询文本转化为向量
        query_vector = self._text_to_vector(query)

        # 在 FAISS 索引中进行搜索，返回的 D 是距离，I 是文档的索引
        D, I = self.index.search(np.array([query_vector]), top_k)

        # 根据索引 I 返回对应的文档内容
        retrieved_docs = [self.documents[i] for i in I[0]]
        return retrieved_docs

    def _text_to_vector(self, text: str) -> np.ndarray:
        return np.random.rand(512)  # 假设文本向量为512维
