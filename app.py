import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFaceHub
from langchain.chains import LLMChain

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"

# Get response from llama-2
def getLLamaResponse(input_text, no_words, blog_style):

    # Model calling
    llm = HuggingFaceHub(repo_id="daryl149/llama-2-7b-chat-hf", model_kwargs={"temperature":0.8, "max_length":4096,"max_new_tokens":4096, "task": "text-generation"})

    # Prompt Template
    template = """
    You are the writing editor which can write the blog. 
    You have to write the blog on {input_text} of word count of {no_words} in such a manner that any topic should be described in form of a story with examples which resonates with the topic.
    Stick with the topic and try to deliver the message from a blog for the described target audience which is {blog_style}. 
    Make the whole blog SEO friendly.
    If the topic is illegal, harmful or vulgure then just respond that "I can not assist you with the illegal, harmful topic. Seeking the information of such topic could indiate a harmful intent."
    """

    prompt = PromptTemplate(template=template,
                            input_variables=['input_text', 'no_words','blog_style'])
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    # Generating the response from llama-2
    # response = llm.invoke(prompt.format(input_text=input_text, no_words=no_words, blog_style=blog_style))
    response = chain.invoke({'input_text': input_text, 'no_words': no_words, 'blog_style':blog_style})
    print(response)

    return response


st.set_page_config(page_title='Blog Generation',
                   page_icon='🤖',
                   layout='centered',
                   initial_sidebar_state='collapsed')

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
    st.write(getLLamaResponse(input_text, no_words, blog_style))