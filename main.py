from googleSearch import *
import os
import streamlit as st
from langchain_community.utilities import GoogleSearchAPIWrapper
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.messages import AIMessage ,HumanMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv('HUGGINGFACEHUB_API_TOKEN')
os.environ["GOOGLE_CSE_ID"] = os.getenv('GOOGLE_CSE_ID')
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')

#object of the class
google_obj= GoogleSearch()

#storing the history in the session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#page confing and title of the page
st.set_page_config(page_title='InfoGenX', page_icon='🤖',)
st.title(':blue[Info-GenX] Blogs 🤖')
st.subheader('Your :green[Content fetching] and :green[Generating] Assistance', divider='rainbow')

with st.expander("About the Bot"):
    st.write("""
        Introducing "Info-GenX" 🤖: Your Ultimate Content Companion

In the fast-paced world of digital content creation, the need for a seamless and efficient writing assistant has never been more apparent. Enter "Info-GenX," a revolutionary tool designed to redefine the way writers, bloggers, and content creators approach their craft.

🚀 Unleashing the Power of Real-Time Information Retrieval:

Info-GenX seamlessly integrates two powerful features—Google Search and AI Content Generation—to provide an unparalleled writing experience. Harness the latest information at your fingertips with a real-time Google search that ensures your content is not only relevant but also up-to-the-minute.

🔍 Supercharged Google Search Results:

Ever wished for a tool that not only fetches Google search results but also transforms them into engaging, informative snippets? Look no further! Info-GenX combines the precision of Google Search with the flair of carefully curated content, delivering results that go beyond conventional search output.

📝 AI-Driven Content Generation:

Inspired by the idea of an intelligent writing companion, Info-GenX employs cutting-edge language models to assist in crafting blog articles, posts, or any written content with ease. Simply input your topic, and watch as the AI weaves a compelling narrative tailored to your needs. It's like having a writing assistant available 24/7.

🌐 Why Info-GenX?

Efficiency Redefined: Save time and effort with a tool that streamlines your content creation process. Let Info-GenX do the heavy lifting, allowing you to focus on what truly matters—your creative expression.

Real-Time Relevance: Keep your content fresh and relevant with real-time Google search results. No more outdated information—Info-GenX ensures your writing stays ahead of the curve.

Tailored to Your Voice: The AI-driven content generation adapts to your writing style, providing personalized assistance that complements your unique voice. It's like having a writing companion that understands you.

SEO-Friendly Blogs: Craft content that not only captivates readers but also appeals to search engines. Info-GenX guides you in creating SEO-friendly blogs that stand out in the vast digital landscape.

🌟 About Us:

As final-year project enthusiasts, we envisioned Info-GenX as a solution to the challenges faced by content creators. With a passion for technology and a commitment to simplifying the content creation journey, we embarked on this project to empower writers with tools that make a difference.

Join us on this exciting journey of creativity, innovation, and efficient content creation with Info-GenX—the ultimate writing companion for the modern content creator! 🚀✨
    """)

#conversation set-up
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

# Get response from model
def getResponse(query,chat_history):

    # Model calling
    llm = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",temperature=0.8,max_new_tokens=4096)

    # Prompt Template
    template = """
        You are the writing editor and can write the blog as if you are an experienced writer.

        Write an article on "{query}". Describe the topic as a story with examples that resonate with the reader. Modify the blog as per the user requirements based on the history of chat.
        
        Chat_history = {chat_history}

        Make the blog SEO-friendly.

        If the topic is illegal, harmful, or vulgar, respond with "I cannot assist you with illegal, harmful topics. Seeking information on such topics could indicate harmful intent."
        """

    prompt = ChatPromptTemplate.from_template(template=template)
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({'chat_history':chat_history , 'query': query})
    
#user input
user_input = st.chat_input("Write the blog/article/post for...")
if user_input is not None and user_input!="":
    st.session_state.chat_history.append(HumanMessage(user_input))
    
    with st.chat_message("Human"):
        st.markdown(user_input)
        
    with st.chat_message("AI"):
        for doc in google_obj.ask_query(user_input):
            st.markdown("### "+ doc["title"])
            st.markdown("- "+ doc["link"])
        #this will return the output same as the chatGPT returning it
        ai_res = st.write_stream(getResponse(user_input, st.session_state.chat_history))
        
    st.session_state.chat_history.append(AIMessage(ai_res))
