import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.documents import Document

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def load_filtered_data(time_limit, cuisine_filter):
    df = pd.read_csv("recipes.csv")

    df = df.dropna(subset=["Cleaned-Ingredients", "TranslatedInstructions", "TranslatedRecipeName"])
    df["TotalTimeInMins"] = pd.to_numeric(df["TotalTimeInMins"], errors="coerce")
    df = df.dropna(subset=["TotalTimeInMins"])
    df = df[df["TotalTimeInMins"] <= time_limit]

    if cuisine_filter.lower() != "any":
        df = df[df["Cuisine"].str.lower() == cuisine_filter.lower()]

    return df

def create_documents_from_df(df):
    documents = []
    for _, row in df.iterrows():
        metadata = {
            "name": row["TranslatedRecipeName"],
            "time": row["TotalTimeInMins"],
            "cuisine": row["Cuisine"]
        }
        content = f"""Recipe: {row['TranslatedRecipeName']}
Ingredients: {row['Cleaned-Ingredients']}
Instructions: {row['TranslatedInstructions']}
Cuisine: {row['Cuisine']}
Time: {row['TotalTimeInMins']} mins
"""
        documents.append(Document(page_content=content, metadata=metadata))
    return documents

def create_vectorstore_and_chain(time_limit, cuisine_filter):
    df = load_filtered_data(time_limit, cuisine_filter)
    docs = create_documents_from_df(df)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    prompt = PromptTemplate(
        input_variables=["context", "input"],
        template="""
You are a smart Indian Recipe AI. Based on the ingredients, suggest the best matching Indian recipe.

Ingredients: {input}

Use the following recipe context to guide your response:
{context}

Return the recipe name, cuisine, total time, and instructions.
"""
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=GOOGLE_API_KEY,
        convert_system_message_to_human=True,
        temperature=0.6
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt}
    )

    return chain
