import streamlit as st
import os

# 업로드시에 "업로드"라는 폴더를 생성하고 그곳에 파일을 보관
# 폴더생성
# 파일저장

HOME = os.getcwd()
# 폴더경로
UPLOAD_DIR = os.path.join(HOME,"uploads")

# 폴더가 없을 시 생성
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# 파일 업로드
uploaded_files = st.file_uploader(
    "Choose a image file", accept_multiple_files=True
)
# 파일을 동시에 여러개 업로드시에는 for를 활용
for uploaded_file in uploaded_files:
    # 업로드 된 데이터를 image에 저장
    # read함수 : 네트워크를 통해 데이터를 가져온다
    image = uploaded_file.read()
    # st.write("filename:", uploaded_file.name)
    # st.write(image)
    st.image(image, caption=uploaded_file.name)

    # 파일 uploads 폴더에 저장
    # wb - 바이너리파일 저장 
    with open(os.path.join(UPLOAD_DIR, uploaded_file.name), "wb") as f:
        f.write(image)
        f.close()