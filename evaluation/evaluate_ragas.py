import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

from app.rag import PyTorchRAG

from ragas.llms import llm_factory
from ragas.embeddings.base import embedding_factory
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
)


load_dotenv()


async def main():

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not found in .env")

    # Load RAG
    rag = PyTorchRAG()

    # Load questions
    questions_path = Path(__file__).parent / "questions.json"

    with open(questions_path, "r", encoding="utf-8") as file:
        questions = json.load(file)

    # Async OpenAI client
    client = AsyncOpenAI()

    # LLM used by RAGAS
    evaluator_llm = llm_factory(
        "gpt-5",
        client=client,
        max_tokens=8192
    )

    # Embeddings used by Answer Relevancy
    evaluator_embeddings = embedding_factory(
        "openai",
        model="text-embedding-3-small",
        client=client
    )

    # Metrics
    faithfulness = Faithfulness(
        llm=evaluator_llm
    )

    answer_relevancy = AnswerRelevancy(
        llm=evaluator_llm,
        embeddings=evaluator_embeddings
    )

    context_precision = ContextPrecision(
        llm=evaluator_llm
    )

    all_faithfulness = []
    all_relevancy = []
    all_precision = []

    # Evaluation
    for i, item in enumerate(questions, start=1):

        question = item["question"]
        reference = item["reference_answer"]

        print(f"\nEvaluating {i}/{len(questions)}")
        print("Question:", question)

        # Generate answer
        result = rag.ask(question)
        answer = result["answer"]

        # Retrieve contexts
        retrieved = rag.retrieve(question)

        contexts = [
            result.chunk.content
            for result in retrieved
        ]

        # Faithfulness
        faithfulness_result = await faithfulness.ascore(
            user_input=question,
            response=answer,
            retrieved_contexts=contexts
        )

        # Answer Relevancy
        relevancy_result = await answer_relevancy.ascore(
            user_input=question,
            response=answer
        )

        # Context Precision
        precision_result = await context_precision.ascore(
            user_input=question,
            reference=reference,
            retrieved_contexts=contexts
        )

        f_score = faithfulness_result.value
        r_score = relevancy_result.value
        p_score = precision_result.value

        all_faithfulness.append(f_score)
        all_relevancy.append(r_score)
        all_precision.append(p_score)

        print("\nAnswer:")
        print(answer)

        print("\nScores:")
        print("Faithfulness:", round(f_score, 3))
        print("Answer Relevancy:", round(r_score, 3))
        print("Context Precision:", round(p_score, 3))

    # Final averages
    print("\n==============================")
    print("FINAL EVALUATION")
    print("==============================")

    print(
        "Average Faithfulness:",
        round(sum(all_faithfulness) / len(all_faithfulness), 3)
    )

    print(
        "Average Answer Relevancy:",
        round(sum(all_relevancy) / len(all_relevancy), 3)
    )

    print(
        "Average Context Precision:",
        round(sum(all_precision) / len(all_precision), 3)
    )


if __name__ == "__main__":
    asyncio.run(main())