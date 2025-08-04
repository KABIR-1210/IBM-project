import streamlit as st
from utils.rag_helper import create_vectorstore_and_chain

# Get query parameters
params = st.query_params
default_time = int(params["time"][0]) if "time" in params and params["time"] and params["time"][0].isdigit() else 60
default_cuisine = params["cuisine"][0] if "cuisine" in params and params["cuisine"] and params["cuisine"][0] else "Any"

# Session state for dark mode
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# Sidebar toggle
st.sidebar.markdown("### UI Settings")
dark_toggle = st.sidebar.checkbox("🌙 Enable Dark Mode", value=st.session_state.dark_mode)

# Apply toggle
st.session_state.dark_mode = dark_toggle

# Apply dark/light theme CSS
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
            body, .stApp {
                background-color: #1e1e1e;
                color: #f0f0f0;
            }
            .stTextInput, .stTextArea, .stSelectbox, .stSlider {
                background-color: #333;
                color: #fff;
            }
            .stButton>button {
                background-color: #ff914d;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
            body, .stApp {
                background-color: #fffaf5;
                color: #333;
            }
            .stButton>button {
                background-color: #ff914d;
                color: white;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# App title
st.title("🍛 Smart Recipe Suggester")

# User input
ingredients = st.text_area("Enter available ingredients (comma-separated):")
time_limit = st.slider("Maximum cooking time (in minutes):", 10, 120, default_time)
cuisine = st.selectbox(
    "Choose cuisine:",
    ["Any", "North Indian", "South Indian", "Gujarati", "Bengali", "Mughlai", "Rajasthani"],
    index=0 if default_cuisine == "Any" else ["Any", "North Indian", "South Indian", "Gujarati", "Bengali", "Mughlai", "Rajasthani"].index(default_cuisine)
)

# Recipe Suggestion Button
if st.button("Suggest Recipes"):
    if ingredients.strip() == "":
        st.warning("Please enter some ingredients.")
    else:
        with st.spinner("Finding the best recipes for you..."):
            try:
                qa_chain = create_vectorstore_and_chain(time_limit, cuisine)
                response = qa_chain.run(ingredients)
                st.success("Here’s a recipe you can try:")
                st.write(response)
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
