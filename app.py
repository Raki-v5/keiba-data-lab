
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="KEIBA DATA LAB",
    page_icon="🏇",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #101010;
    color: #ffffff;
}
h1, h2, h3 {
    color: #D8B45A !important;
}
.gold {
    color: #D8B45A;
}
div[data-testid="stMetric"] {
    background: #211D14;
    border: 1px solid #806B3D;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    "<h1>♛ KEIBA DATA LAB</h1>",
    unsafe_allow_html=True
)
st.caption("RACING INTELLIGENCE SYSTEM")
st.markdown("---")

st.subheader("TODAY'S RACE")

race = st.selectbox(
    "分析するレース",
    ["園田 9R", "園田 10R", "中央競馬 重賞"]
)

st.markdown("### レース分析")
st.info("現在は画面確認用のサンプルデータです。実際の競馬データではありません。")


if st.session_state.get("registered_horses"):
    horses = pd.DataFrame(st.session_state.registered_horses)
    horses["能力評価"] = 0
    horses["予測勝率(%)"] = 0.0
else:
    horses = pd.DataFrame(columns=[
        "馬番", "馬名", "騎手", "単勝オッズ",
        "能力評価", "予測勝率(%)"
    ])

horses["期待値"] = (
    horses["予測勝率(%)"] / 100
    * horses["単勝オッズ"]
)

st.markdown("### ANALYSIS RANKING")

mode = st.radio(
    "分析方法",
    ["データ評価", "期待値評価"],
    horizontal=True
)

if mode == "データ評価":
    result = horses.sort_values(
        "能力評価", ascending=False
    )
    st.caption("過去成績などから馬の能力を評価するランキング")
    st.dataframe(
        result[["馬番", "馬名", "能力評価"]],
        hide_index=True,
        use_container_width=True
    )

else:
    result = horses.sort_values(
        "期待値", ascending=False
    )
    st.caption("独自予測勝率と単勝オッズから算出")
    st.dataframe(
        result[[
            "馬番", "馬名", "予測勝率(%)",
            "単勝オッズ", "期待値"
        ]],
        hide_index=True,
        use_container_width=True
    )

st.markdown("---")
st.subheader("DATA MANAGEMENT")

col1, col2, col3 = st.columns(3)

col1.metric("分析対象", "5頭")
col2.metric("評価方式", "2種類")
col3.metric("データ状況", "サンプル")

st.markdown("---")
st.markdown(
    "<center style='color:#D8B45A'>"
    "KEIBA DATA LAB<br>"
    "DATA × ANALYSIS × EXPECTED VALUE"
    "</center>",
    unsafe_allow_html=True
)
st.markdown("---")
st.subheader("🏇 出走馬データ登録")

st.caption("出走馬を登録して一覧表に追加できます。")

if "registered_horses" not in st.session_state:
    st.session_state.registered_horses = []

with st.form("horse_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        number = st.number_input(
            "馬番", min_value=1, max_value=18, value=1
        )
        name = st.text_input("馬名")

    with col2:
        jockey = st.text_input("騎手名")
        odds = st.number_input(
            "単勝オッズ", min_value=0.0, value=1.0
        )

    submitted = st.form_submit_button("出走馬を登録")

    if submitted:
        if not name.strip():
            st.error("馬名を入力してください。")

        elif any(
            h["馬番"] == number
            for h in st.session_state.registered_horses
        ):
            st.error("その馬番はすでに登録されています。")

        else:
            st.session_state.registered_horses.append({
                "馬番": number,
                "馬名": name.strip(),
                "騎手": jockey,
                "単勝オッズ": odds
            })
            st.success(f"{name} を登録しました！")

st.markdown("### 📋 登録済み出走馬")

if st.session_state.registered_horses:
    registered_df = pd.DataFrame(
        st.session_state.registered_horses
    )
    st.dataframe(
        registered_df,
        hide_index=True,
        use_container_width=True
    )
    st.caption(
        f"現在 {len(registered_df)} 頭登録されています。"
    )
else:
    st.info("まだ出走馬が登録されていません。")




