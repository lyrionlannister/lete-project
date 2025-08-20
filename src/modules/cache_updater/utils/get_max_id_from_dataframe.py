import pandas as pd

async def get_max_id_from_dataframe(df: pd.DataFrame, primary_key: str) -> int:
    """
    Returns the maximum ID from a DataFrame.
    """

    if primary_key not in df.columns:
        raise ValueError(f"Primary key '{primary_key}' not found in DataFrame columns.")
    
    if df.empty:
        return 0
    return int(df[primary_key].max())