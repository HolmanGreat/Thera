#Importing dependencies
import os
import streamlit as st
import googletrans



from googletrans import Translator
from gtts import gTTS


# Importing Langchain Modules
#from langchain_community.llms import ctransformers
#from langchain.chains import LLMChain
#from langchain.prompts import PromptTemplate
#from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from llama_cpp import Llama
#import huggingface-hub


#HUGGINGFACE CREDENTIALS
headers = { "authorization":st.secrets["auth_token"], "content-type": "application/json"}

#SELECTING MODEL
llm = Llama.from_pretrained(
    repo_id="Qwen/Qwen1.5-0.5B-Chat-GGUF",
    filename="*q8_0.gguf")
    #repo_id="BioMistral/BioMistral-7B-GGUF",
    #filename="ggml-model-Q4_K_M.gguf")




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
        tab1, tab2 = st.tabs(["Contact A Doctor", "What's New"])

        with tab1:
            st.header("Speak To A Doctor")
            st.image("istockphoto-1679775124-612x612.jpg")
            contact= st.selectbox("Language",["🤍English","💙Francais/Arabic","💛Portuguese","❤️Swahili"])
            if contact == "🤍English":
                st.link_button("Contact A Doctor", "https://zoiehealth.com/")
            elif contact == "💙Francais/Arabic":
                st.link_button("Contacter un médecin/التحدث إلى الطبيب", "https://www.ahkili.com.tn/")
            elif contact == "💛Portuguese":
                st.link_button("Fale com um médico", "https://appysaude.co.ao/")
            elif contact == "❤️Swahili":
                st.link_button("Zungumza na Daktari","https://medikea.co.tz/")
        
        with tab2:
            st.header("What's New")
            st.image("Screenshot_2024_0323_223748.png", caption = "💖#IWD2024")
            st.write("Wishing all the incredible women out there a Happy International Women's Day! May this day be filled with recognition, appreciation, and inspiration as we honor the achievements and resilience of women worldwide. Here's to breaking barriers, shattering stereotypes, and creating a brighter, more inclusive future for all. 🌟👩‍🎓👩‍⚕️👩‍🔬👩‍💼👩‍🔧👩‍🌾👩‍🏫👩‍🎨👩‍✈️👩‍🚀👩‍⚖️🌍")
            
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
                response_in_english = extracted_english_text

                output = llm.create_chat_completion(
                    messages=[
                        {"role": "system", "content": "You are a helpful AI chatbot, answer politely"},
                        {"role": "user", "content": response_in_english}
                     ]
                )
                # Accessing the 'content' key within the 'message' dictionary
                response_content = output['choices'][0]['message']['content']
                response_in_userlang = translator.translate(response_content, src = "en", dest = default_lang_detected)
                output_text = response_in_userlang.text
                st.markdown(output_text)

                
                #Converting text to speech
                text_to_speech = gTTS(text = output_text,
                                          lang = default_lang_detected,
                                          slow = False)

                text_to_speech.save("speech.wav")
                st.audio("speech.wav")



            



    

            #Add ChatBot's Response To Chat History
            st.session_state.messages.append({"role":"assistant","content":output_text})






if __name__ == '__main__':
    main()




#st.link_button("🔵🔴 Contacter un médecin", "https://www.clickdoc.ma/")
#st.link_button("⚪🟢Contact A Doctor", "https://www.quromedical.com.za")
#st.link_button("⚪Contact A Mental Health Physician", "https://www.innersparkrecovery.com")
#st.link_button("🔵🔴Médecin en santé mentale", "https://www.ahkili.com.tn/")
#st.link_button("⚪Mental Health Physician", "https://nguvuhealth.com/" )
#st.link_button("🟠 Fale com um médico", "https://appysaude.co.ao/")
#st.link_button("🔵⚪ Contact A Doctor", "https://www.waspito.com")
#st.link_button("⚪🟢 Contact A Doctor", "https://www.clafiya.com")
#st.link_button("🔴🔵 التحدث إلى الطبيب ", "https://www.dabadoc.com")
    




             

         

                
