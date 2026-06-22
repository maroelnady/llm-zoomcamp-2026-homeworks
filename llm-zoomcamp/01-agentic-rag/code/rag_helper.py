INSTRUCTIONS = '''
Your task is to answer questions from the course participants
based on the provided context.

Use the context to find relevant information and provide accurate
answers. If the answer is not found in the context,
respond with "I don't know."
'''

PROMPT_TEMPLATE = '''
QUESTION: {question}

CONTEXT:
{context}
'''.strip()


class RAGBase:
     def __init__(
        self,
        index,
        llm_client,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        #course='llm-zoomcamp',
        model='gemini-2.5-flash'
    ):
        self.index = index
        self.llm_client = llm_client
        self.instructions = instructions
        self.course = course
        self.prompt_template = prompt_template
        self.model = model

    def search(self, query, num_results=5):
    return self.index.search(
        query,
        num_results=num_results
    )

    def build_context(self, search_results):
        lines = []

        for doc in search_results:
            lines.append(doc['section'])
            lines.append('Q: ' + doc['question'])
            lines.append('A: ' + doc['answer'])
            lines.append('')

        return '\n'.join(lines).strip()

    def build_prompt(self, query, search_results):
        context = self.build_context(search_results)
        return self.prompt_template.format(
            question=query, context=context
        )

    def llm(self, prompt):
        input_messages = [
            {'role': 'developer', 'content': self.instructions},
            {'role': 'user', 'content': prompt}
        ]

        response = self.llm_client.responses.create(
            model=self.model,
            input=input_messages
        )

        return response.output_text




    #      # =========================================================
    # # FIX: Updated to support the Google GenAI Client Structure
    # # =========================================================
    # def llm(self, prompt):
    #     # 1. Package instructions inside a Configuration block
    #     config = types.GenerateContentConfig(
    #         system_instruction=self.instructions
    #     )

    #     # 2. Call generate_content via the client instance
    #     response = self.llm_client.models.generate_content(
    #         model=self.model,
    #         contents=prompt,
    #         config=config
    #     )

    #     # 3. Return response text using .text instead of .output_text
    #     return response.text

    def rag(self, query):
        search_results = self.search(query)
        prompt = self.build_prompt(query, search_results)
        answer = self.llm(prompt)
        return answer


#   def rag(self, question):
#     context = self.build_context(question)

#     prompt = self.build_prompt(question, context)

#     response = self.llm(prompt)

#     return response.output_text, response.usage