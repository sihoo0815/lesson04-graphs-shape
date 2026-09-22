import pandas as pd
import plotly.express as px
import streamlit as st


# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/"
    "kobis_movies.csv"
)


# -----------------------------
# 제목
# -----------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("1년간 박스오피스 10위권에 든 영화 데이터를 그래프로 살펴봅니다.")


# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일: 여덟 자리 숫자를 날짜형으로 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce",
    )

    # 여러 장르가 "|"로 연결된 경우 첫 번째 장르만 사용
    df["genre_first"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    return df


try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
    st.stop()


# -----------------------------
# 간단한 데이터 안내
# -----------------------------
st.write(
    f"전체 영화 **{len(df):,}편**을 대상으로 장르별 분포를 살펴봅니다."
)


# ============================================================
# 그래프 1. 장르별 영화 편수
# ============================================================
st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre_first"]
    .value_counts()
    .rename_axis("genre")
    .reset_index(name="count")
)

genre_counts["ratio"] = genre_counts["count"] / genre_counts["count"].sum()


fig = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수",
)

fig.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    ),
)

fig.update_layout(
    height=500,
    margin=dict(t=70, b=20, l=20, r=20),
    legend_title="장르",
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displayModeBar": False},
)


# -----------------------------
# 그래프 해석 입력 영역
# -----------------------------
st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 정리해 보세요.",
    placeholder="예: 가장 많은 영화가 속한 장르는 ○○이고, 전체 영화의 약 ○○%를 차지한다.",
    height=90,
    label_visibility="collapsed",
)


st.divider()


# -----------------------------
# 데이터 표
# -----------------------------
with st.expander("원본 데이터 일부 보기"):
    display_columns = [
        "movieCd",
        "movieNm",
        "openDt",
        "genre",
        "nation",
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10",
    ]

    display_df = df[display_columns].copy()
    display_df["openDt"] = display_df["openDt"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )
