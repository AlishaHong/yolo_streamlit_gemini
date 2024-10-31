import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# 환경 변수 로드 (API 키 불러오기)
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 파일 업로드 함수
def upload_to_gemini(path, mime_type=None):
    """Gemini에 파일을 업로드합니다."""
    file = genai.upload_file(path, mime_type=mime_type)
    st.write(f"파일 '{file.display_name}'이(가) 업로드되었습니다: {file.uri}")
    return file

# 모델 설정
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# 스트림릿 인터페이스 구성
st.title("레시피 생성기")
st.write("아래에 이미지를 업로드하고 레시피를 생성하세요.")

# 이미지 업로드 인터페이스
uploaded_files = st.file_uploader("이미지를 업로드하세요", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

# 이미지가 업로드되었을 때 실행되는 부분
if uploaded_files:
    files = []
    for uploaded_file in uploaded_files:
        # 파일을 임시로 저장
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Gemini에 파일 업로드
        files.append(upload_to_gemini(uploaded_file.name, mime_type="image/jpeg"))
    
    # 텍스트 입력란에 메뉴 이름 입력
    menu_name = st.text_input("메뉴 이름을 입력하세요:", "라면")

    # 레시피 생성 버튼
    if st.button("레시피 생성"):
        # 모델을 통해 레시피 생성
        response = model.generate_content([
            "input: ", menu_name, files[0], 
            "output: 메뉴 : " + menu_name + "\n1. 재료: ...\n2. 조리순서: ...",
        ])
        
        # 결과 출력
        st.write("### 생성된 레시피")
        st.write(response.text)
