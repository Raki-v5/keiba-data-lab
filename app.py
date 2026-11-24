
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

horses = pd.DataFrame({
    "馬番": [7, 3, 5, 1, 9],
    "馬名": [
        "サンプルホースA",
        "サンプルホースB",
        "サンプルホースC",
        "サンプルホースD",
        "サンプルホースE"
    ],
    "能力評価": [94, 87, 79, 71, 65],
    "予測勝率(%)": [29, 21, 16, 9, 7],
    "単勝オッズ": [3.2, 8.5, 12.0, 25.0, 6.0]
})

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
