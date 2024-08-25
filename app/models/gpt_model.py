import os
from openai import OpenAI


class GPTModel:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_code(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a handy assistant that generates Python code. Generate code only."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        # return response['choices'][0]['message']['content'].strip()
        return response.choices[0].message.content.strip()
