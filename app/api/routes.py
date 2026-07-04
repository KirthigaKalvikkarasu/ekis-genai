from fastapi import APIRouter

from app.pipeline.ingestion_pipeline import IngestionPipeline
from app.pipeline.retrieval_pipeline import RetrievalPipeline
from app.llm.generator import LLMGenerator
from app.llm.guardrails import validate_response

router = APIRouter()
file_location = "/Users/kirthiga.kalvikkarasu/Projects/ekis-genai/app/tests/sample_document.pdf"

# Initialize once (simulate pre-indexed data)
ingestion_pipeline = IngestionPipeline()
records = ingestion_pipeline.run(file_location)

retrieval_pipeline = RetrievalPipeline(records)
generator = LLMGenerator()


@router.post("/query")
def query_system(query: str):

    # Retrieve context
    results = retrieval_pipeline.run(query)

    context_chunks = [r["text"] for r in results]

    # Generate answer
    response = generator.generate(query, context_chunks)

    # Validate
    validate_response(response)

    return {
        "answer": response,
        "context_used": results
    }