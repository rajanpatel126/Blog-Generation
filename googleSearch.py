import os
from langchain_community.utilities import GoogleSearchAPIWrapper
from dotenv import load_dotenv
from langchain.tools import Tool
load_dotenv()

os.environ["GOOGLE_CSE_ID"] = os.getenv('GOOGLE_CSE_ID')
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

#google search class fetching data results
class GoogleSearch():
    tool=None
    
    def make_model(self):

        # Tool integration
        def top5_results(query):
            search = GoogleSearchAPIWrapper()
            return search.results(query, 5)

        GoogleSearch.tool = Tool(
            name="Google Search Snippets",
            description="Search Google for top results.",
            func=top5_results,
        )
        
    def ask_query(self,query:str):
        if GoogleSearch.tool is None: 
            self.make_model()
        return GoogleSearch.tool.run(query)
    