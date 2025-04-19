import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# ページ全体の設定とカスタムCSS
st.set_page_config(
    page_title="AI専門家アシスタント",
    page_icon="🧠",
    layout="wide"
)

# カスタムCSSを追加
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0D47A1;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .expert-card {
        background-color: #f0f8ff;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #1E88E5;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .expert-selected {
        background-color: #e3f2fd;
        border-left: 5px solid #64B5F6;
    }
    .response-container {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #4CAF50;
    }
    .stButton > button {
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        background-color: #0D47A1;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .info-box {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .app-description {
        margin-bottom: 2rem;
        color: #555;
        line-height: 1.6;
    }
    footer {
        text-align: center;
        margin-top: 3rem;
        color: #666;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# タイトルと説明の設定
st.markdown("<h1 class='main-header'>🧠 AI専門家アシスタント</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    st.markdown("""
    <div class="app-description">
    さまざまな専門分野のAIアシスタントに質問できるプラットフォームへようこそ。
    AI専門家に質問することで、専門知識に基づいた回答を得ることができます。
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box" style="background-color: #e3f2fd; padding: 15px; border-radius: 10px;">
    <b>💡 使用方法：</b><br>
    1. 下記の専門家から話したい専門家を選択します<br>
    2. 質問や相談したい内容を入力フォームに記入します<br>
    3. 送信ボタンをクリックして回答を取得します
    </div>
    """, unsafe_allow_html=True)

# 専門家の定義
experts = {
    "A": {
        "name": "医療専門家",
        "icon": "🩺",
        "description": "健康や医学に関する一般的な情報を提供します",
        "system_message": "あなたは医学の専門知識を持つ医療専門家です。医学的な質問に対して、科学的根拠に基づいた正確な情報を提供してください。ただし、これは医師による診断や治療の代わりにはならないことを明確にしてください。"
    },
    "B": {
        "name": "法律専門家",
        "icon": "⚖️",
        "description": "法的な一般情報を提供します",
        "system_message": "あなたは法律の専門知識を持つ法律専門家です。法的な質問に対して一般的な情報を提供してください。ただし、これは正式な法的アドバイスではなく、具体的な状況に応じた専門家への相談を推奨してください。"
    },
    "C": {
        "name": "テクノロジー専門家",
        "icon": "💻",
        "description": "テクノロジーに関する質問に答えます",
        "system_message": "あなたはAI、プログラミング、ハードウェア、ソフトウェアなどのテクノロジーに関する深い知識を持つテクノロジー専門家です。技術的な質問に対して正確で実用的な情報を提供してください。"
    },
    "D": {
        "name": "ビジネス専門家",
        "icon": "📊",
        "description": "ビジネス戦略や経営に関するアドバイスを提供します",
        "system_message": "あなたは経営戦略、マーケティング、財務などのビジネスに関する専門知識を持つビジネス専門家です。ビジネスに関する質問に対して実践的で戦略的なアドバイスを提供してください。"
    }
}

# LLMの初期化
def initialize_llm():
    """LLMモデルを初期化する関数"""
    return ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0.7
    )

# LLMに質問する関数
def ask_llm(expert_key, user_input):
    """
    選択された専門家の種類とユーザー入力に基づいてLLMから回答を取得する
    
    Parameters:
    expert_key (str): 選択された専門家のキー (A, B, C, D)
    user_input (str): ユーザーが入力したテキスト
    
    Returns:
    str: LLMからの回答
    """
    if not user_input.strip():
        return "質問を入力してください。"
    
    # 専門家の情報を取得
    expert_info = experts[expert_key]
    
    # LLMの初期化
    llm = initialize_llm()
    
    # メッセージの作成
    messages = [
        SystemMessage(content=expert_info["system_message"]),
        HumanMessage(content=user_input)
    ]
    
    # LLMに質問して回答を取得
    try:
        response = llm(messages)
        return response.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

# Streamlit UIの構築
def main():
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        # 専門家選択のセクション
        st.markdown("<h2 class='sub-header'>専門家を選択</h2>", unsafe_allow_html=True)
        
        # 専門家選択のラジオボタン（通常の表示に戻す）
        expert_options = {f"{key}: {expert['icon']} {expert['name']}": key for key, expert in experts.items()}
        selected_expert_option = st.radio(
            "",
            list(expert_options.keys()),
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # 選択された専門家のキー (A, B, C, D) を取得
        selected_expert_key = expert_options[selected_expert_option]
        selected_expert = experts[selected_expert_key]
        
        # 専門家カードを表示
        st.markdown(f"""
        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; margin: 20px 0;">
            <b>💬 現在の専門家:</b> {selected_expert['icon']} <b>{selected_expert['name']}</b><br>
            <p style="margin-top: 10px; margin-bottom: 0;">{selected_expert['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 質問セクション
        st.markdown("<h2 class='sub-header'>質問入力</h2>", unsafe_allow_html=True)
        
        # ユーザー入力フォーム（明示的にtext_areaを使用）
        user_input = st.text_area(
            "専門家に質問したい内容を入力してください",
            height=150,
            key="user_input",
            placeholder=f"{selected_expert['icon']} {selected_expert['name']}に質問したいことを入力..."
        )
        
        # 送信ボタン
        col1, col2, col3 = st.columns([4, 2, 4])
        with col2:
            send_button = st.button("送信", type="primary", use_container_width=True)
        
        # 回答表示セクション
        if send_button:
            if not user_input.strip():
                st.warning("⚠️ 質問を入力してください")
            else:
                with st.spinner(f"{selected_expert['icon']} 回答を生成中..."):
                    # LLMからの回答を取得
                    response = ask_llm(selected_expert_key, user_input)
                    
                    # 回答を表示
                    st.markdown("<h2 class='sub-header'>回答</h2>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="response-container">
                        {response}
                    </div>
                    """, unsafe_allow_html=True)
        
        # フッター
        st.markdown("""
        <footer>
            <hr>
            <p>AI専門家アシスタント © 2025 | Powered by LangChain & OpenAI</p>
        </footer>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()