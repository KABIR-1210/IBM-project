import pandas as pd
from langchain_core.documents import Document

def load_dataset(path="recipes.csv"):
    df = pd.read_csv(path)

    # Drop rows missing key data
    df = df.dropna(subset=["Cleaned-Ingredients", "TranslatedInstructions", "TranslatedRecipeName"])

    documents = []
    for _, row in df.iterrows():
        content = f"""Recipe: {row['TranslatedRecipeName']}
Ingredients: {row['Cleaned-Ingredients']}
Instructions: {row['TranslatedInstructions']}
Cuisine: {row.get('Cuisine', 'Unknown')}
Time: {row.get('TotalTimeInMins', 'Unknown')} mins
"""
        metadata = {
            "name": row['TranslatedRecipeName'],
            "cuisine": row.get("Cuisine", "Unknown"),
            "time": row.get("TotalTimeInMins", "Unknown")
        }
        documents.append(Document(page_content=content, metadata=metadata))

    return documents
