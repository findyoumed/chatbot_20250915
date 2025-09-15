import streamlit as st
from openai import OpenAI

# 페이지 기본 설정
st.set_page_config(page_title="😂 유머 챗봇", page_icon="😂", layout="centered")

# CSS 스타일 추가 (말풍선 형태)
st.markdown(
    """
    <style>
    .chat-bubble {
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px 0;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-bubble {
        background-color: #DCF8C6; /* 카톡 사용자 색상 */
        text-align: right;
        margin-left: auto;
    }
    .assistant-bubble {
        background-color: #FFFFFF;
        border: 1px solid #ddd;
        text-align: left;
        margin-right: auto;
    }
    .chat-container {
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 타이틀 & 설명
st.title("😂 오늘의 유머 챗봇")
st.write("하루를 웃음으로 채워줄 **아재개그/유머 챗봇**이에요! 대화는 카톡 느낌으로 진행됩니다 📱")

# API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key 입력", type="password")
if not openai_api_key:
    st.info("먼저 API 키를 입력해주세요! 키 없이는 농담도 못해요 🤭", icon="🗝️")
else:
    # OpenAI 클라이언트
    client = OpenAI(api_key=openai_api_key)

    # 초기 메시지 (system + 첫 응답)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "너는 유머러스하고 친근한 농담 전문 챗봇이야. 카톡 대화체처럼 재밌게 말해."},
            {"role": "assistant", "content": "안녕하세요! 😂 오늘도 빵 터질 준비됐나요?\n👉 세상에서 제일 뜨거운 과일은? 천도복숭아 🔥🍑"}
        ]

    # 기존 대화 출력 (말풍선 스타일 적용)
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f"<div class='chat-bubble assistant-bubble'>🤖 {message['content']}</div>", unsafe_allow_html=True)
        elif message["role"] == "user":
            st.markdown(f"<div class='chat-bubble user-bubble'>🧑 {message['content']}</div>", unsafe_allow_html=True)

    # 입력창
    if prompt := st.chat_input("😎 유머, 아재개그, 썰 다 받아요!"):
        # user 메시지 저장 + 출력
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.markdown(f"<div class='chat-bubble user-bubble'>🧑 {prompt}</div>", unsafe_allow_html=True)

        # OpenAI 응답 (스트리밍)
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # assistant 응답 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})

    # 푸터
    st.markdown("---")
    st.caption("🤣 Powered by GPT & Streamlit | 웃으면 복이 와요 ✨")
