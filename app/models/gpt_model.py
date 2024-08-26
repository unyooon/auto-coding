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
                {"role": "system",
                    "content": "You are a handy assistant that generates code. Generate code only. Not include back quotes."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=16384,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def generate_json(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                    "content": "You are a handy assistant that generates json. Generate json only. Not include back quotes.\nformat is `[{file_path: str, description: str}]`"},
                {"role": "user", "content": prompt},
            ],
            max_tokens=16384,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    def generate(self, prompt: str, max_tokens: int = 150) -> str:
        """
        プロンプトに基づいてテキストを生成するメソッド。
        :param prompt: テキスト生成のためのプロンプト。
        :param max_tokens: 生成される最大トークン数。
        :return: 生成されたテキスト。
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # もしくは適切なエンジンを指定
                messages=[
                    {"role": "system",
                        "content": "You are a handy assistant that generates text. Generate text only. Not include back quotes."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except:
            print(f"Error generating text")
            return ""
