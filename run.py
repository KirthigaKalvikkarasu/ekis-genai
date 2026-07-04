from app.pipeline.ingestion_pipeline import IngestionPipeline
from app.pipeline.retrieval_pipeline import RetrievalPipeline
from app.llm.generator import LLMGenerator
from app.llm.guardrails import validate_response

file_location = "/Users/kirthiga.kalvikkarasu/Projects/ekis-genai/app/tests/sample_document.pdf"


def main():
    print(" Running ingestion pipeline...")

    ingestion = IngestionPipeline()
    records = ingestion.run(file_location)

    print(f" Loaded {len(records)} chunks")

    retrieval = RetrievalPipeline(records)

    query = input("\n Enter your question: ")

    print("\n Retrieving context...")
    results = retrieval.run(query)

    context = [r["text"] for r in results]

    print("\n Generating answer...")
    generator = LLMGenerator()
    response = generator.generate(query, context)

    validate_response(response)

    print("\n FINAL ANSWER:")
    print(response)

    print("\n CONTEXT USED:")
    for r in results:
        print("-", r["metadata"]["source"], "| score:", r.get("rerank_score", 0))


if __name__ == "__main__":
    main()