import streamlit as st
import os

# 앱 제목 설정
st.title("음료 자판기")

# 현재 디렉토리에서 이미지 경로 설정
HOME = os.getcwd()
cider_Path = os.path.join(HOME, 'data', 'cider.jpg')
coke_Path = os.path.join(HOME, 'data', 'coke.jpg')
fanta_Path = os.path.join(HOME, 'data', 'fanta.jpg')

# 음료 이미지와 재고 정의
images = {
    "사이다": cider_Path,
    "콜라": coke_Path,
    "환타": fanta_Path
}

# Streamlit 상태 유지 기능을 사용하여 재고를 유지
if 'stock' not in st.session_state:
    st.session_state.stock = {
        "사이다": 10,
        "콜라": 10,
        "환타": 10
    }

# 선택된 음료 저장
selected_choice = st.session_state.get('selected_choice', None)
choice = None
cols = st.columns(3)
for i, (name, img_url) in enumerate(images.items()):
    with cols[i]:
        st.image(img_url, use_column_width=True)    #use_column_width = False하면 이미지 대박 커짐
        st.write(f"재고: {st.session_state.stock[name]}개")
        if st.session_state.stock[name] > 0:
            if st.button(f"{name}", key=f"btn_{name}", use_container_width=True): #use_container_width = false하면 작은 버튼생성
                st.session_state.stock[name] -= 1
                st.session_state.selected_choice = name
                st.rerun()  # 이 코드가 없으면 바로 업데이트 되지 않는다. 
                # st.experimental_rerun()   # 최신버전에서는 이 코드를 사용할 수 있다. 

# 재고가 없는 음료에 대해 경고 표시
out_of_stock = [name for name, count in st.session_state.stock.items() if count == 0]
if out_of_stock:
    st.warning(" / ".join(out_of_stock) + " 재고 없음")

# 선택된 음료 이미지 출력
if 'selected_choice' in st.session_state and st.session_state.selected_choice:
    choice = st.session_state.selected_choice
    st.subheader(f"선택된 음료: {choice}")
    st.image(images[choice], caption=choice, use_column_width=True)

