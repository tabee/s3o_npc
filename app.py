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

def generate_tweet(text_input_medienmitteilung, result_top3keywords, result_facts):
    # result_tweets: write 3 matching tweets for a specific media release, facts, keywords.
    prompt = PromptTemplate.from_template("""
        You are a neutral media spokesperson for the Federal Council 
        and write 3 matching tweets for a specific media release.
        
        Your tweets always contain:
        1. the 2 most important facts
        2. the 3 most important keywords
        3. 4 matching emojis.
        4. the tweet ends with the string [url].

        Rules:
        You answer in the same language as the media release.

        Sources: 
        ===========
        Facts: {facts}
        Top-Keywords: {top3keywords}
        Media release: {medienmitteilung}
        ==============
        Your 3 different tweet suggestions:
    """)
    runnable = prompt | ChatOpenAI(model=model) | StrOutputParser()
    result_tweets = runnable.invoke({"medienmitteilung": text_input_medienmitteilung, "top3keywords": result_top3keywords, "facts": result_facts})
    print(result_tweets)
    return result_tweets

def generate_questions(text_input_medienmitteilung, result_top3keywords, result_facts):
    # result_fragen_reporter1: from 20min.ch/Wagenknecht and will collect 3 critical questions. 
    prompt = PromptTemplate.from_template("""
        You are a reporter (male) for 20min.ch and 
        will collect 10 critical questions. 
        At the end we need the 3 most critical 
        questions.

        You think like Sahra Wagenknecht. 

        It is important that the questions 
        directly to the press release.
        
        Important:
        The questions are critical but not offensive. 
        and refer to the media release, the facts and a top keyword.

        Rules:
        Answer in the same language as the media release.

        Sources: 
        ===========
        Facts: {facts}
        Top-Keywords: {top3keywords}
        Media release: {medienmitteilung}
        ==============
        Your top-5 moust critical questions:
    """)
    runnable = prompt | ChatOpenAI(model=model) | StrOutputParser()
    result_fragen_reporter1 = runnable.invoke({"medienmitteilung": text_input_medienmitteilung, "top3keywords": result_top3keywords, "facts": result_facts})
    print(result_fragen_reporter1)
    return result_fragen_reporter1

def generate_summary(text_input_medienmitteilung, result_facts):
    # result_zusammenfassung_kind: summary for a 10 year old child 
    prompt = PromptTemplate.from_template("""
    Create a summary of the following text 
        for a 10 year old child of a media release.

        Important rule:
        Answer in the same language as the media release!

        Sources: 
        ===========
        Facts: {facts}
        Media release: {medienmitteilung}
        ==============
        Your child-friendly summary in correct language:
    """)
    runnable = prompt | ChatOpenAI(model=model) | StrOutputParser()
    result_zusammenfassung_kind =  runnable.invoke({"medienmitteilung": text_input_medienmitteilung, "facts": result_facts})
    print(result_zusammenfassung_kind)
    return result_zusammenfassung_kind

def generate_dallE_prompt(result_zusammenfassung_kind,result_top3keywords,result_facts):
    # result_dalle3prompt: DALL-E prompt : black and white comic book panel in style of asterix & obelix in mid-21th 
    # copy-paste the result_dalle3prompt into a good image generator like Midjourney or DallE-3 
    prompt = PromptTemplate.from_template("""
    Create a prompt to generate 
        with DALL-E a matching image.
        the prompt must be child-friendly.

        Important Roules:
        =================
        1) Your DALL-E Prompt must be in english.
        2) It must include the following texts:
            A)"create a black and white comic book panel"
            B)"comic illustration reminiscent of European adventure comics of the mid-21th century"
            C)"in a informative way." 
            D) [SCENE]
            E) The scene plays in switzerland.
            F) Prompt must be length 1000 or less.
        3) "Include a dramatic sound effect text saying &quot;{top3keywords}&quot;
        =================

        Contextinformation for the [SCENE]: {zusammenfassung_kind}
        ==============
        Generated the [SCENE] and following the rules 1-3!
        ==============
        Your DALL-E Prompt follows rules 1-3:
    """)
    runnable = prompt | ChatOpenAI(model=model) | StrOutputParser()
    result_dalle3prompt =  runnable.invoke({"zusammenfassung_kind": result_zusammenfassung_kind, "top3keywords": result_top3keywords, "facts": result_facts})
    print(result_dalle3prompt)
    return result_dalle3prompt


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
    ("gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4-0613", "gpt-4"))


def generate_response(input_text):
    """Generates a response from the OpenAI API."""
    medienmitteilung = input_text
    result_facts = None
    
    with st.chat_message("System", avatar="🤖"):
        
        st.write("Analyze input ... ")
        
        with st.expander("facts"):
            result_facts = analyze_text(input_text)
            st.write(result_facts)
        
        with st.expander("keywords"):
            keywords = generate_10_keywords(result_facts)
            st.write(keywords)
        
        with st.expander("top_keywords"):
            top_keywords = generate3keywords(medienmitteilung, keywords)
            st.write(top_keywords)
        
        with st.expander("tweets"):
            tweets = generate_tweet(medienmitteilung, top_keywords, result_facts)
            st.write(tweets)
        
        with st.expander("questions"):
            questions = generate_questions(medienmitteilung, top_keywords, result_facts)
            st.write(questions)

        with st.expander("summary"):
            summary = generate_summary(medienmitteilung, result_facts)
            st.write(summary)

        with st.expander("dall E 3 prompt"):
            dallE3_prompt = generate_dallE_prompt(summary,top_keywords,result_facts)
            st.write(dallE3_prompt)

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
        with st.chat_message("System", avatar="🤖"):
            st.write('Please enter your OpenAI API key! Navigate to the openai website to get one.')
