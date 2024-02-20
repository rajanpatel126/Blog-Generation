import streamlit as st
import os
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper

load_dotenv()

os.environ["GOOGLE_CSE_ID"] = os.getenv('GOOGLE_CSE_ID')
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')


#tool integration

def top5_results(query):
    search = GoogleSearchAPIWrapper()
    return search.results(query, 5)

def main():
    st.title("Google Search Results App")

    # User input for the query
    query = st.text_input("Enter your search query:")

    
    tool = Tool(
    name="Google Search Snippets",
    description="Search Google for top results.",
    func=top5_results,
    )

    # Button to trigger the search
    if st.button("Generate"):
        if query:
            result = tool.run(query, verbose=True)
            
    # Display the results
            st.subheader("Top 5 Google Search Results:")
            for i, result in enumerate(iterable=result):
                st.write(f"{i+1}. {result}")
        else:
            st.warning("Please enter a search query.")
    
if __name__ == "__main__":
    main()
