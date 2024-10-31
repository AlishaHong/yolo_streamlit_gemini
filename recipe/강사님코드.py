import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Function to upload a file to Gemini
def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    st.write(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Function to generate content
def generate_recipe_response(files):
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

    # Generate content based on inputs
    response = model.generate_content([
        "input: ", "라면", files[0],
        "output: 메뉴 : 라면\n1. 재료라면 1봉지스프 1/2개대파 1뿌리올리브유 2스푼2. 조리순서1. 평소대로 물을 550ml 넣고 끓여주세요    2. 끓는 물에 라면과 스프를 넣어주세요    여기서 포인트는 라면을 70~80%만 익혀주시는거에요,이따가 라면 볶으면서 또 익혀줄거기 때문에 푹 익히면퍼질 수가 있어요~!포인트는 라면을 70~80%만 익히기3. 살짝 덜 익은 라면 물을 버려주세요그 때 라면 국물 3~4스푼은 남겨주시고 버려주세요^^    4. 이제 팬에 올리브유 or 식용유 2스푼을 올려주세요    5. 다음 아까 설익은 라면을 넣고 볶아줄거에요그리고 아까 라면 끓는 물 3~4스푼 기억나시죠?^^6. 끓인 물 4스푼을 함께 넣어서 약불에서 볶아주세요~    7. 다음 대파를 올려주시구요~~8. 대파향이 솔솔~~ 날때까지 볶아주세요저는 백종원 레시피중에 가장 마음에 드는게 대파향인거 같아요 ㅎㅎ원래 파를 좋아하기도 하지만 대파향 솔솔 나는게 참 좋아요    9. 다음 라면스프 1/2을 넣고 샤샤샥~ 볶아주세요10. 조금 더 넣으면 혹시 짤수가 있으니 드셔보시면서 조절하는걸로~^^    짠~! 완성되었어요,",
        "input: ", "제육볶음", files[1],
        "output: ",
    ])

    return response.text

# Streamlit app layout
st.title("Recipe Generation with Gemini AI")

# Upload files
st.write("Upload images for '라면' and '제육볶음'")
ramen_file = st.file_uploader("Upload image for 라면", type=['jpg', 'jpeg'])
jeyuk_file = st.file_uploader("Upload image for 제육볶음", type=['jpg', 'jpeg'])

# Process if both files are uploaded
if ramen_file and jeyuk_file:
    # Save uploaded files to a temporary path
    ramen_path = f"temp_ramen.jpg"
    jeyuk_path = f"temp_jeyuk.jpg"
    with open(ramen_path, "wb") as f:
        f.write(ramen_file.getbuffer())
    with open(jeyuk_path, "wb") as f:
        f.write(jeyuk_file.getbuffer())

    # Upload files to Gemini
    files = [
        upload_to_gemini(ramen_path, mime_type="image/jpeg"),
        upload_to_gemini(jeyuk_path, mime_type="image/jpeg"),
    ]

    # Generate and display response
    st.write("Generating recipe response...")
    response_text = generate_recipe_response(files)
    st.write("Generated Recipe Response:")
    st.text(response_text)
else:
    st.write("Please upload both images to proceed.")
