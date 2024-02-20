import streamlit as st
import os
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_community.utilities import GoogleSearchAPIWrapper

load_dotenv()

os.environ["GOOGLE_CSE_ID"] = os.getenv('GOOGLE_CSE_ID')
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

# Tool integration
def top5_results(query):
    search = GoogleSearchAPIWrapper()
    return search.results(query, 5)

# Function to store results and queries in session state
def get_session_results():
    if 'queries' not in st.session_state:
        st.session_state.queries = []
    if 'results' not in st.session_state:
        st.session_state.results = []

def main():
    st.title("Google Search Results App")

    # Initialize session state
    get_session_results()

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
            # Store the query in session state
            st.session_state.queries.append(query)

            # Run the tool and store the result in session state
            results = tool.run(query, verbose=True)
            st.session_state.results.append(results)

    # Display the results history
    st.subheader("Search History:")
    for i, (query, result) in enumerate(reversed(list(zip(st.session_state.queries, st.session_state.results))),start=1):
        st.write(f"{i}. Query: {query}")
        st.subheader("Results:")
        for j, result_item in enumerate(result):
            st.markdown(f"   **{j+1}. Title:** {result_item.get('title', '')}")
            if 'link' in result_item:
                st.write(f"      **URL:** {result_item['link']}")
            if 'snippet' in result_item:
                st.write(f"      **Snippet:** {result_item['snippet']}")
            st.write("   ----")

if __name__ == "__main__":
    main()
