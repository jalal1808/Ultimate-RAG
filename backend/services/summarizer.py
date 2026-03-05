import pandas as pd
from backend.services import text_chunker
from backend.services.generator import generate_text
from backend.services.table_reasoner import answer_from_table

CHUNK_SUMMARY_PROMPT = (
    "You are a document summarization assistant. Summarize the following text concisely:\n\n"
    "{chunk_text}\n\n"
    "SUMMARY:"
)


def summarize_text(text: str) -> str:
    """
    Map-reduce summarization for long text documents.
    1. Chunk the text
    2. Summarize each chunk individually with Gemini
    3. Combine all chunk summaries
    4. Final summarization pass on combined text
    """
    chunks = text_chunker.chunk_text(text, file_id="summary_doc")

    if not chunks:
        return "Document is empty. Nothing to summarize."

    # Step 2: Summarize each chunk individually
    chunk_summaries = []
    for chunk in chunks:
        prompt = CHUNK_SUMMARY_PROMPT.format(chunk_text=chunk["text"])
        summary = generate_text(prompt)
        chunk_summaries.append(summary.strip())

    # Step 3: Combine all chunk summaries
    combined = "\n\n".join(chunk_summaries)

    # Step 4: Final pass over combined summaries
    final_prompt = (
        "You are a document summarization assistant. "
        "Produce a concise, coherent final summary of the following:\n\n"
        f"{combined}\n\n"
        "FINAL SUMMARY:"
    )
    return generate_text(final_prompt).strip()


def summarize_table(df: pd.DataFrame) -> str:
    """
    Statistical + semantic overview of a DataFrame.
    Delegates to table_reasoner for Gemini-powered summary.
    """
    if df.empty:
        return "The table is empty. No summary can be produced."

    query = "Provide a concise summary of this dataset, highlighting key statistics, patterns, and notable observations."
    return answer_from_table(query, df).strip()
