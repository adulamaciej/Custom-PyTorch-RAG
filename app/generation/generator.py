from openai import OpenAI

from app.generation.prompts import (
    SYSTEM_PROMPT,
    build_prompt
)


class Generator:

    def __init__(
        self,
        model="gpt-5.6-luna"
    ):
        self.client = OpenAI()
        self.model = model

    def generate(
        self,
        question,
        context
    ):
        prompt = build_prompt(
            question,
            context
        )

        response = self.client.responses.create(
            model=self.model,
            instructions=SYSTEM_PROMPT,
            input=prompt
        )

        return response.output_text