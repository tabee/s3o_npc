import os
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser

def analyze_text(text_input_medienmitteilung):
    # result_facts: Analyze the following text and identify all important facts
    prompt = PromptTemplate.from_template("""
    Analyze the following text and 
        identify all important facts.  
        The text is from news.admin.ch and is an 
        official media release: \n {medienmitteilung}\n\n
        rule: answer in same language as the media release!
        Your fact analysis:
    """)
    runnable = prompt | ChatOpenAI(model=model) | StrOutputParser()
    result_facts = runnable.invoke({"medienmitteilung": text_input_medienmitteilung})
    print(result_facts)
    return result_facts

def generate_10_keywords(result_facts):
    # result_top10keywords: Identify 10 keywords from the facts
    prompt = PromptTemplate.from_template("""
        Identify 10 keywords that are likely to rank well 
        on Google (Switzerland). 
        The keywords are in the same language as the 
        following text and start with a #.

        Text: 
        {facts}
        
        Examples: #FederalCouncil #Geneva #Nyon #Motorway #A1 #Traffic #Trafficflow #Motorway     
        Your keywords incl. #:
    """)
    runnable = prompt | ChatOpenAI(model=model) | StrOutputParser()
    result_top10keywords = runnable.invoke({"facts": result_facts})
    print(result_top10keywords)
    return result_top10keywords

def generate3keywords(text_input_medienmitteilung, result_top10keywords):
    # result_top3keywords: Analyze the following keywords and text. 
    prompt = PromptTemplate.from_template("""
        Analyze the following keywords and text. 
        Identify exactly 3 keywords that can rank 
        well on Google (Switzerland). 

        Examples: #FederalCouncil #ChuckNorris #Thailand  (on one line)
    
        ===============
        Keywords: 
        {top10keywords}

        Text: 
        {medienmitteilung}
        ===============
        Your top 3 keywords in the same language as the text/keywords:
    """)
    runnable = prompt | ChatOpenAI(model=model) | StrOutputParser()
    result_top3keywords = runnable.invoke({"medienmitteilung": text_input_medienmitteilung, "top10keywords": result_top10keywords})
    print(result_top3keywords)
    return result_top3keywords

# Streamlit App
st.title('s3o npc 🤖')

load_dotenv()
# Konfigurationsbereich in der Sidebar
openai_api_key = st.sidebar.text_input(
    'OpenAI API Key',
    value='',
    type='password')
optimize_input = st.sidebar.toggle('autopilot', value=True, disabled=True)
model = st.sidebar.radio( 
    "Choose a model:",
    ("gpt-3.5-turbo", "gpt-4"))





def generate_response(input_text):
    medienmitteilung = input_text
    result_facts = analyze_text(input_text)
    with st.chat_message("System", avatar="🤖"):
        st.write(f"analyze_text\n: {result_facts}")

    keywords = generate_10_keywords(result_facts)
    with st.chat_message("System", avatar="🤖"):
        st.write(f"keywordst\n: {keywords}")
        
    top_keywords = generate3keywords(medienmitteilung, keywords)
    with st.chat_message("System", avatar="🤖"):
        st.write(f"top keywordst\n: {top_keywords}")



# Willkommensnachricht
with st.chat_message("System", avatar="🤖"):
    st.write("copy and paste a media release in message box and start...")

# Chat Eingabebereich
prompt = st.chat_input("Enter your message")
if prompt:
    with st.chat_message("User"):
        st.write(prompt)
    
    if openai_api_key.startswith('sk-'):
        generate_response(prompt)
    if not openai_api_key.startswith('sk-'):
        with st.chat_message("System", avatar="🧙‍♂️"):
            st.write('Please enter your OpenAI API key! Navigate to the openai website to get one.')
