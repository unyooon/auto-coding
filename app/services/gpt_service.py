from app.models.gpt_model import GPTModel


class GPTService:
    def __init__(self):
        self.model = GPTModel()

    def generate_code(self, instruction: str) -> str:
        prompt = f"Generate a Python code that does the following:\n{
            instruction}"
        return self.model.generate_code(prompt)

    def generate_code_from_markdown(self, markdown_text: str) -> str:
        prompt = f"Generate a Nuxt 3 component or page based on the following Markdown description:\n{
            markdown_text}"
        return self.model.generate_code(prompt)
