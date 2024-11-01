# st_chatbot.py
import google.generativeai as genai 
import streamlit as st
from dotenv import load_dotenv
import os

# 라이브러리 설명
# google.generativeai: Google Generative AI 라이브러리 - ai 모델 사용
# dotenv :.env 파일에서 환경변수를 로드

load_dotenv() # .env 파일에서 GEMINI_API_KEY를 로드
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))    # 값 읽어와서 설정

st.title("Gemini-Bot")

# streamlit 캐싱 
# 함수가 호출될 때마다 모델을 다시 로드하지 않도록 한 번만 실행된 결과를 캐싱
@st.cache_resource
def load_model():
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("model loaded...")
    return model

model = load_model()

# Streamlit의 session_state는 세션을 유지하는 변수 저장소
# "chat_session"이 없으면 새 대화 세션을 시작
if "chat_session" not in st.session_state:    
    st.session_state["chat_session"] = model.start_chat(history=[]) 

for content in st.session_state.chat_session.history:
    with st.chat_message("ai" if content.role == "model" else "user"):
        st.markdown(content.parts[0].text)

if prompt := st.chat_input("메시지를 입력하세요."):    
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("ai"):
        response = st.session_state.chat_session.send_message(prompt)        
        st.markdown(response.text)