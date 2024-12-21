# app/models/rag_model.py

from app.models.LLM.llm_model import LLMClient
from app.models.RAG.retrieval.query_handler import QueryHandler

class RAGModel:
    def __init__(self, llm_model: LLMClient, retriever: QueryHandler):
        self.llm_model = llm_model
        self.retriever = retriever

    def generate_answer_with_context(self, query: str, top_k: int = 5) -> str:
        # 检索相关文档
        retrieved_docs = self.retriever.retrieve(query, top_k=top_k)
        # 组合查询与检索到的文档
        context = "\n".join(retrieved_docs)
        prompt = f"Question: {query}\n\nContext: {context}\n\nAnswer:"
        # 使用 LLM 生成答案
        return self.llm_model.generate_answer(prompt)
