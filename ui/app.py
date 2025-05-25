import streamlit as st
import aiohttp
import asyncio

st.title("Executive Orders Query System")

async def query_api(query):
    async with aiohttp.ClientSession() as session:
        async with session.post("http://localhost:8000/query", json={"query": query}) as response:
            return await response.json()

query = st.text_input("Enter your query:")
if st.button("Submit"):
    if query:
        try:
            response = asyncio.run(query_api(query))
            st.write(response.get("response", "Error fetching response"))
        except Exception as e:
            st.write(f"Error: {str(e)}")
    else:
        st.write("Please enter a query.")