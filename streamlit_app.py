import streamlit as st
import garage_ai.vector_db.db as db

st.set_page_config(page_title="Garage.ai")

if query := st.chat_input("Type a query..."):
    st.write(query)