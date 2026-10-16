import os
import streamlit as st
from groq import Groq

# Page Configuration & Clean Styling
st.set_page_config(
    page_title="Noyan's AI Mark 2", page_icon="💻", layout="centered"
)

hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Smart Language System Prompt
system_prompt = {
    "role": "system",
    "content": (
        "Tumhara naam Noyan's AI Mark 2 hai. Tumhein Shariq Noyan ne banaya"
        " hai. Tum kisi bhi doosri company ya ChatGPT ka naam nahi loge. "
        "Language Rule: Agar user Roman Urdu (English alphabets mein Urdu)"
        " mein baat kare, toh tum bhi Roman Urdu mein jawab doge. Agar user"
        " English mein baat kare, toh tum English mein jawab doge."
    ),
}

# Sidebar mein New Chat button
with st.sidebar:
  st.title("Menu")
  if st.button("New Chat 🗑️"):
    st.session_state.messages_mark2 = [system_prompt]
    st.rerun()

# App Title & Subtitle
st.title("Noyan's AI Mark 2")
st.write("Yahan har sawal ka jawab milega—bas logic ki umeed mat rakhna.")

# Groq API Key check
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
  st.error("API Key missing! Please set GROQ_API_KEY in Streamlit Secrets.")
else:
  client = Groq(api_key=api_key)

  # Chat History Session State
  if "messages_mark2" not in st.session_state:
    st.session_state.messages_mark2 = [system_prompt]

  # Display prior chat history
  for message in st.session_state.messages_mark2:
    if message["role"] != "system":
      avatar = "👤" if message["role"] == "user" else "🤖"
      with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

  # Chat input box
  if prompt := st.chat_input("Apna sawal yahan likhein..."):
    st.session_state.messages_mark2.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
      st.markdown(prompt)

    # Generate response from Groq
    with st.chat_message("assistant", avatar="🤖"):
      with st.spinner("Soch raha hai..."):
        try:
          completion = client.chat.completions.create(
              model="openai/gpt-oss-120b",
              messages=[
                  {"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages_mark2
              ],
              temperature=0.7,
          )
          response = completion.choices[0].message.content
          st.markdown(response)

          st.session_state.messages_mark2.append(
              {"role": "assistant", "content": response}
          )
        except Exception as e:
          st.error(f"Error: {e}")