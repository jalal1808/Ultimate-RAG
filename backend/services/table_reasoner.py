import pandas as pd
from backend.services.generator import generate_text

def answer_from_table(query: str, df: pd.DataFrame) -> str:
    """
    Answer a natural language query using pandas operations.
    Returns a descriptive answer string with explanation.
    """
    if df.empty:
        return "The table is empty. No computations can be performed."

    profile = _profile_dataframe(df)
    prompt = _build_table_prompt(query, profile, df)
    return generate_text(prompt)

def _profile_dataframe(df: pd.DataFrame) -> str:
    """
    Generate a text summary of the dataframe schema and stats.
    Used to give Gemini context about the table structure.
    """
    lines = []

    # Shape
    rows, cols = df.shape
    lines.append(f"Rows: {rows}, Columns: {cols}")

    # Column names and dtypes
    col_types = ", ".join(f"{col} ({df[col].dtype})" for col in df.columns)
    lines.append(f"Columns: {col_types}")

    # Sample first 3 rows
    sample = df.head(3).to_string(index=False)
    lines.append("Sample (first 3 rows):")
    lines.append(sample)

    # Numeric statistics with nulls
    numeric_cols = df.select_dtypes(include=["number"])
    if not numeric_cols.empty:
        lines.append("Numeric stats:")
        for col in numeric_cols.columns:
            col_data = numeric_cols[col]
            min_val = col_data.min()
            max_val = col_data.max()
            mean_val = col_data.mean()
            nulls = col_data.isnull().sum()
            lines.append(
                f"  {col}: min={min_val}, max={max_val}, mean={mean_val:.2f}, nulls={nulls}"
            )

    return "\n".join(lines)


def _build_table_prompt(query: str, profile: str, df: pd.DataFrame) -> str:
    """
    Build the RAG-style prompt for table reasoning.
    Keeps sample small (3 rows) to avoid context overflow.
    """
    return (
        "You are a data analyst. A user has asked a question about a dataset.\n"
        "Use the table profile and sample below to answer accurately.\n"
        "Explain HOW you arrived at the answer (what computation you performed).\n\n"
        "TABLE PROFILE:\n"
        f"{profile}\n\n"
        f"QUESTION: {query}\n\n"
        "ANSWER (include reasoning):"
    )