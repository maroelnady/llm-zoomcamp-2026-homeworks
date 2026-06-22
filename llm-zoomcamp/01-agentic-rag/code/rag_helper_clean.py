from google import genai

class RAGBase:
    def __init__(self, index, llm_client, model="gemini-2.5-flash"):
        self.index = index
        self.llm_client = llm_client
        self.model = model

    # ---------------------------
    # SEARCH (clean - no filters)
    # ---------------------------
    def search(self, query, num_results=5):
        return self.index.search(
            query,
            num_results=num_results
        )

    # ---------------------------
    # BUILD CONTEXT
    # ---------------------------
    def build_context(self, search_results):
        context = []

        for doc in search_results:
            context.append(
                f"Filename: {doc['filename']}\n"
                f"Content:\n{doc['content']}"
            )

        return "\n\n---\n\n".join(context)

    # ---------------------------
    # LLM CALL (returns full response)
    # ---------------------------
    def llm(self, prompt):
        response = self.llm_client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response

    # ---------------------------
    # RAG PIPELINE
    # ---------------------------
    def rag(self, query):
        search_results = self.search(query)
        context = self.build_context(search_results)

        prompt = f"""
You are a helpful assistant.

Use the context below to answer the question.

CONTEXT:
{context}

QUESTION:
{query}
"""

        response = self.llm(prompt)

        answer = response.text
        usage = getattr(response, "usage_metadata", None)

        return answer, usage