from googleSearch import GoogleSearch
import os
import streamlit as st
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain_core.messages import AIMessage ,HumanMessage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv('HUGGINGFACEHUB_API_TOKEN')

#object of the class
google_obj= GoogleSearch()

#storing the history in the session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?"),
    ]

#page confing and title of the page
st.set_page_config(page_title='Info-GenX', page_icon='🤖',)
st.title(':blue[Info-GenX] Blogs 🤖')
st.subheader('Your :green[Content Fetching] and :green[Generating] Assistance', divider='rainbow')
st.caption("Info-GenX can make mistakes. Consider checking important information.")

#sample Prompts
prompts = [
    "Let's talk about superheroes and their powers!",
    "Explain the concept of blockchain technology and its applications in finance.",
    "I want to know about dinosaurs and fossils!",
    "Explore the implications of climate change on global food security.",
    "Tell me a story about magical creatures in a enchanted forest!",
    "Discuss the impact of social media on modern marketing strategies."
]

st.markdown("***Here are some sample Prompts***\n" + "\n".join([f"- {prompt}" for prompt in prompts]))

with st.expander("About the Bot"):
    st.write("""
        Introducing "Info-GenX" 🤖: Your Ultimate Content Companion

        In the fast-paced world of digital content creation, the need for a seamless and efficient writing assistant has never been more apparent. Enter "Info-GenX," a revolutionary tool designed to redefine the way writers, bloggers, and content creators approach their craft.

        🚀 Unleashing the Power of Real-Time Information Retrieval:

        Info-GenX seamlessly integrates two powerful features— Internet Search and AI Content Generation—to provide an unparalleled writing experience. Harness the latest information at your fingertips with a real-time Web search that ensures your content is not only relevant but also up-to-the-minute.

        🔍 Supercharged Web Search Results:

        Ever wished for a tool that not only fetches Web search results but also transforms them into engaging, informative snippets? Look no further! Info-GenX combines the precision of complete Internet Search with the flair of carefully curated content, delivering results that go beyond conventional search output.

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
        You are the professional writing editor and can write the blogs or articles. You have to address the audience from a small kid to a professional user so that they all can understand the answer.

        Make the blog SEO-friendly.
        
        Write the article on "{query}". While writing the article on the given topic, describe the topic with examples that resonate with the reader. Start with general information or examples so that any user can relate and understand the topic. As the article goes, you need to go in more and more indepth with the topic. So that you can justice with the topic and user can see satisfied with the answer. 
        
        In response, The first line of the article must be the title of the article in double quote starting with: Title: "title" and then onwards just give one article in the answer. The title should not be mentioned anywhere else in the article. You are not allowed to mentioned the title anywhere else.
        
        Don't make the response feel like a history lesson. The target audience of the blog post is 18-40 years old ranges people, so give mature content, not a kid like content.
        
        Once the whole article finished, you must provide the SEO key words you have used in the article. It should be writtern only once the article finished, not in the middle. 
        
        Do not write meta description and additional notes in the answer, anywhere. 
        
        If user ask you to write in language other than English, simply return "I can only Understand English and not any other language."
        
        Overall, in the answer there should be firstly Title, secondly the Article and then conclude with SEO key words used in the last. After SEO keywords, you have to stop answering further. There is no need to write anything after that.
        
        In brief, The answer must be like you are having the conversation with the user. Do not write formal lines in the answers. The article word count should be 500 words, if word length not specified in the query.
        
        If continuos question are asking, then from the chat history, replay the answer based on the history accordingly.
        Chat_history = {chat_history}
        """

    prompt = ChatPromptTemplate.from_template(template=template)
    chain = prompt | llm | StrOutputParser()
    
    response = chain.stream({'chat_history':chat_history , 'query': query})
    
    response = (text.replace('</s>', '') for text in response)
    response = (text.replace('Ass ert:', '') for text in response)
    response = (text.replace('Answer:', '') for text in response)
    return response
    
#user input
user_input = st.chat_input("Write your blog topic or article idea...")
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
