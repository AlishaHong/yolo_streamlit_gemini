# st_chatbot.py
import google.generativeai as genai 
import streamlit as st
from dotenv import load_dotenv
import os

# 라이브러리 설명
# google.generativeai: Google Generative AI 라이브러리 - ai 모델 사용
# dotenv :.env 파일에서 환경변수를 로드

# 모델의 설정
generation_config = {
  # 온도가 올라가면 예측이 어렵고 낮으면 쉬워진다.
  "temperature": 1,
  # 확률분포내에서 선택할 단어의 범위를 결정 
  "top_p": 0.95,
  # 확률분포내에서 선택할 단어의 수를 결정
  "top_k": 64,
  # 응답메세지의 최대 토큰수
  "max_output_tokens": 8192,
  # 응답메세지의 데이터타입
  "response_mime_type": "text/plain",   # 타입 바꿀 수 있음
}


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
# 두명 이상이 접속했을 경우 세션 관리하는 방법 공식문서 찾아보기 
if "chat_session" not in st.session_state:    
    st.session_state["chat_session"] = model.start_chat(history=[]) 

# 기존코드
# for content in st.session_state.chat_session.history:
#     with st.chat_message("ai" if content.role == "model" else "user", avatar = 'C:/Users/Sesame/YOLO_streamlit/chatbot/dog.jpg'):
#         st.markdown(content.parts[0].text)



# 세션에서도 아바타가 유지되도록 추가 
for content in st.session_state.chat_session.history:
    # AI와 사용자를 구분하여 다른 아바타를 적용
    if content.role == "model":  # AI 메시지
        with st.chat_message("ai", avatar="C:/Users/Sesame/YOLO_streamlit/chatbot/ai.jpg"):
            st.markdown(content.parts[0].text)
    else:  # 사용자 메시지
        with st.chat_message("user", avatar="C:/Users/Sesame/YOLO_streamlit/chatbot/dog.jpg"):
            st.markdown(content.parts[0].text)

if prompt := st.chat_input("메시지를 입력하세요."):    
    with st.chat_message("user", avatar = 'C:/Users/Sesame/YOLO_streamlit/chatbot/dog.jpg'):
        st.markdown(prompt)
    with st.chat_message("ai", avatar="C:/Users/Sesame/YOLO_streamlit/chatbot/ai.jpg"): # avatat = 이모지 넣을 수 있음
        response = st.session_state.chat_session.send_message(prompt)        
        st.markdown(response.text)
# send_message(prompt)를 호출해 AI 모델의 응답을 생성하고, 
# 이를 st.markdown(response.text)로 화면에 출력
