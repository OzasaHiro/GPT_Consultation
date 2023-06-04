import openai
import streamlit as st
from streamlit_chat import message
import os 
from dotenv import load_dotenv
load_dotenv('api_key.env')

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_response(prompt):
    completion=openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    message=completion.choices[0].text
    return message

def get_completion(prompt, model="gpt-3.5-turbo",temperature=0): # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def ProposeSolution(text):
    prompt = f"""
    Create solution for decribed in the review text: 
    
    Make your response as short as possible.
    
    Review Text: ```{text}```
    """
    message = get_completion(prompt)
    #convert response to string
    message = str(message)
    
    return message 


st.title("ChatGPT-Security Consulting")
#storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
user_input=st.text_input("You:",key='input')
if user_input:
    output=ProposeSolution(user_input)
    #store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
#        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
