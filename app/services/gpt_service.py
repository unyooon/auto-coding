from app.models.gpt_model import GPTModel


class GPTService:
    def __init__(self):
        self.model = GPTModel()

    def generate_code(self, instruction: str) -> str:
        prompt = f"Generate a Python code that does the following:\n{
            instruction}"
        return self.model.generate_code(prompt)
