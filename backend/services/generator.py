import google.generativeai as genai
from backend.config import get_settings

_client = None


def _get_client():
    """Configure and return Gemini client"""
    global _client
    if _client is None:
        settings = get_settings()
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _client = genai.GenerativeModel(settings.GEMINI_MODEL)
    return _client

def generate_text(prompt: str) -> str:
    """Generic text generation — accepts any prompt string"""
    model = _get_client()
    response = model.generate_content(prompt)
    return response.text

def generate_answer(query: str, context_chunks: list[dict]) -> str:
    """
    Build context from reranked chunks, ask Gemini to answer.
    Returns grounded answer string.
    """
    if not context_chunks:
        return "No relevant content found in the document."
    context = _build_context(context_chunks)
    prompt = _build_prompt(query, context)
    return generate_text(prompt) 


def _build_context(chunks: list[dict]) -> str:
    """Join chunk texts into a numbered context block"""
    lines = [f"[{i+1}] {chunk['text']}" for i, chunk in enumerate(chunks)]
    return "\n".join(lines)


def _build_prompt(query: str, context: str) -> str:
    return (
        "You are a document analysis assistant. Answer the question using ONLY the context below.\n"
        "If the answer is not in the context, say \"I cannot find this information in the document.\"\n\n"
        "CONTEXT:\n"
        f"{context}\n\n"                      
        f"QUESTION: {query}\n\n"              
        "ANSWER:"
    )