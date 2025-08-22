# 🍛 Recipe Agent – Smart Recipe Suggestions Based on Ingredients

A smart AI-powered recipe suggestion web app that provides personalized Indian recipes based on the ingredients you have. Built with Streamlit, Gemini (Google Generative AI), and FAISS for fast recipe retrieval.

## 🚀 Features

- 🔎 Suggests Indian recipes based on user-provided ingredients
- 🕒 Filter by maximum cooking time
- 🌍 Filter by cuisine type (North Indian, South Indian, etc.)
- 🌙 Default **Dark Mode** UI with toggle support
- ⚡ Fast and efficient recipe retrieval using FAISS vector search
- 🤖 RAG (Retrieval-Augmented Generation) powered by Gemini Pro

## 🧠 How It Works

1. User inputs available ingredients.
2. Gemini Pro uses embedded context from recipe data.
3. The app retrieves the best-matching recipes using FAISS similarity search.
4. The response includes recipe name, cuisine, cooking time, and instructions.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Responsive UI with filters, toggles)
- **Backend:** Python + Gemini Pro API (RAG-based model)
- **Embeddings:** Google Generative AI Embeddings
- **Vector Store:** FAISS (in-memory, fast similarity search)
- **Data:** `recipes.csv` – Cleaned dataset of Indian recipes
- **Others:** `.env` for secure API key loading

---

## 📂 Project Structure

```bash
.
├── main.py                  # Streamlit frontend & backend
├── recipes.csv              # Indian recipe dataset
├── utils/
│   ├── data_loader.py       # Loads and filters recipes
│   └── rag_helper.py        # Creates vectorstore and QA chain
├── requirements.txt         # Required packages
└── .env                     # Contains your Google API Key


