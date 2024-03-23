#Importing dependencies
import os
import streamlit as st
import googletrans



from googletrans import Translator
from gtts import gTTS


# Importing Langchain Modules
from langchain_community.llms import ctransformers
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


#HUGGINGFACE CREDENTIALS
os.environ["HUGGINGFACE_API_TOKEN"] = "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"


#SELECTING MODEL
llm = ctransformers(model="TheBloke/zephyr-7B-beta-GGUF", callbacks=[StreamingStdOutCallbackHandler()])




template = """Question: {question}

Answer:"""

prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(prompt=prompt, llm=llm)













#User Interface


def main():
    app_mode = st.sidebar.selectbox("Menu",["🏡Home","🩺Contact A Doctor","📋About"])


    st.markdown("<h1 style='text-align: center; color: blue;'>Thera</h1>", unsafe_allow_html=True)

    # Center-align the warning message
    st.markdown("<p style='text-align: center; font-size: small; color: red;'>⚠️ Warning: This chatbot provides health information for educational purposes only. It does not offer medical diagnosis or professional advice. Click on the sidebar to consult a healthcare professional for personalized guidance on your health.</p>", unsafe_allow_html=True)



    #About Page
    if app_mode == "📋About":
        st.image("Thera.png",caption ="#Stay Strong...Stay Informed")
        st.write("Thera is your trusted AI companion in women's health. Thera is an AI-powered healthcare chatbot dedicated to enhancing the well-being of women by providing access to reliable health information and connecting them to healthcare professionals when needed.")
        st.image("purple.png", caption = "Empowering Women's Health with AI...Embark on a journey of informed decisions, better health, and well-being. Your health matters, and Thera is here to support you every step of the way.")

        st.image("serene.png", caption = "Together, we can make women's health a priority, and ensure that every woman is empowered with the knowledge and resources she needs to thrive.")
        st.write("#Stay Strong... Stay Informed")

        st.markdown("""
        ---
        We would like to hear from you 🌍 (https://forms.gle/8ZGhZ8Lkkcq43dyG7)
        """)

    #Contact A Doctor
    elif app_mode == "🩺Contact A Doctor":
        st.image("doctor.png")
        st.link_button("💻Speak To A Doctor","https://wallet.clafiya.com/auth/registration")
    elif app_mode == "🏡Home":
        #Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        #Display Chat messages from history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


        #User Input
        if user_question:= st.chat_input("Message Thera"):
            #Add user Input To Chat History
            st.session_state.messages.append({"role":"user", "content":user_question})
            #Display User Input In Chat Message Container
            with st.chat_message("user"):
                st.markdown(user_question)


            #Detecting language of user's query
            translator = Translator()
            user_text = user_question
            detected_language = translator.detect(user_text)
            default_lang_detected = detected_language.lang




            #Translate user's question to English text
            english_text = translator.translate(user_text, src = default_lang_detected, dest = "en")
            extracted_english_text = english_text.text






            #ChatBot's Response

            #Display ChatBot's Response In Message Container
            with st.chat_message("assistant"):
                #Setup Callback Handler For streaming response
                #st_callback = StreamlitCallbackHandler(st.container())

                #Pass extracted_english_text to LLM
                response_in_english = llm_chain.run(extracted_english_text)


                response_in_userlang = translator.translate(response_in_english, src = "en", dest = default_lang_detected)
                output_text = response_in_userlang.text
                st.markdown(output_text)


            #Add ChatBot's Response To Chat History
            st.session_state.messages.append({"role":"assistant","content":output_text})






if __name__ == '__main__':
    main()
