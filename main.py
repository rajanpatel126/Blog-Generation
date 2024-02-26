import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.chains import LLMChain
from dotenv import load_dotenv
from googleSearch import *

google_obj= GoogleSearch()

load_dotenv()

st.set_page_config(page_title='Blog Generation',
                   page_icon='🤖',
                   layout='wide',
                   initial_sidebar_state='collapsed')

# Get response from model
def getResponse(input_text, no_words, blog_style):

    # Model calling
    llm = HuggingFaceEndpoint(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",temperature=0.8,max_new_tokens=4096)

    # Prompt Template
    template = """
        You are the writing editor and can write the blog as if you are an experienced writer.

        Write an article on "{input_text}" with the word count of {no_words}. Describe the topic as a story with examples that resonate with the reader. Stay on topic and deliver the message in a blog format suitable for the target audience: {blog_style}.

        Make the blog SEO-friendly.

        If the topic is illegal, harmful, or vulgar, respond with "I cannot assist you with illegal, harmful topics. Seeking information on such topics could indicate harmful intent."
        """


    prompt = PromptTemplate(template=template,
                            input_variables=['input_text', 'no_words','blog_style'])
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    
    response = chain.invoke({'input_text': input_text, 'no_words': no_words, 'blog_style':blog_style})
    # print(response)

    return response['text']


st.header('GenX Blogs 🤖')

input_text = st.text_input("Enter your blog topic")

# Creating two more additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of words: ')
with col2:
    blog_style = st.selectbox('Target Audience for the blog: ',
                              ('Professionals', 'Academics', 'General Public', 'Undergraduate', 'k-12'),
                              index=2)

submit = st.button('Generate')

# Output
if submit:
    with st.spinner("generating..."):
        for doc in google_obj.ask_query(input_text):
            st.markdown("### "+ doc["title"])
            st.markdown("- "+ doc["link"])
        st.markdown(getResponse(input_text, no_words,blog_style))