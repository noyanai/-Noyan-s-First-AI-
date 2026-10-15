from groq import Groq
import streamlit as st

# Page ki settings
st.set_page_config(page_title="Mera Fast AI Tutor", page_icon="⚡")

st.title("⚡ Mera Ultra-Fast AI Tutor (Groq Powered)")
st.write(
    "Yeh cloud par chalta hai, isliye bina laptop ko garam kiye ek second mein"
    " jawab dega!"
)

# Secure tareeqay se .streamlit/secrets.toml se API key uthana
try:
  GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception as e:
  st.error(
      "API Key nahi mili! Check karo ke .streamlit folder mein secrets.toml"
      " file theek bani hai ya nahi."
  )
  st.stop()

# User se input lene ke liye text box
user_topic = st.text_input("Tumhein kis topic ke baray mein janna hai?", "")

if st.button("Jawab Do 🚀"):
  if user_topic.strip() == "":
    st.warning("Pehle koi topic toh likho bhai!")
  else:
    with st.spinner("Groq rocket ki speed se soch raha hai... ⚡"):
      try:
        # Secure key ke sath client initialize karna
        client = Groq(api_key=GROQ_API_KEY)

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Mujhe '{user_topic}' ke baray mein aasan Urdu/Roman"
                        " Urdu mein tafseel se aur seedha jawab do. Repeat mat"
                        " karna."
                    ),
                }
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        st.success("Yeh lo lightning-fast jawab:")
        st.write(completion.choices[0].message.content)

      except Exception as e:
        st.error(f"Masla aa gaya: {e}")