# Chatbot for Learners, Readers, Writers, Authors, and Poets

- This bot will answer respond to your query by generating the article, story, blog post, so on and so fourth in a SEO friendly manner.
- The answer will also fetch the top 5 articles related to your query from the whole Internet.
- So, Content Fetching and Generation: Two results at the same time.

## Requirements

### Python Version

- [python 3.9.13](https://www.python.org/downloads/release/python-3913/)

### Huggingface API

- Generate your API key and place it in the .streamlit/secrets.toml file:
  [env]
  HUGGINGFACEHUB_API_TOKEN="your_huggingfacehub_api_key"

## Setup Environment

### Steps

- Create a virtual environment:
  bash
  python -m venv venv
- Activate virtual environment:
  bash
  venv\Scripts\Activate.ps1
- Install Python modules:
  bash
  python -m pip install -r "requirements.txt"