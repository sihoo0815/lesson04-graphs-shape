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
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일을 날짜형으로 변환
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

    # 총 관객을 숫자로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce",
    ).fillna(0)

    return df


# -----------------------------
# 데이터 준비
# -----------------------------
try:
    df = load_data()
except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.exception(e)
    st.stop()


# -----------------------------
# 제목
# -----------------------------
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.caption("1년간 박스오피스 10위권에 든 영화 데이터를 그래프로 살펴봅니다.")

st.write(
    f"전체 영화 **{len(df):,}편**을 대상으로 장르와 관객 분포를 살펴봅니다."
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

fig_genre = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수",
)

fig_genre.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    ),
)

fig_genre.update_layout(
    height=500,
    margin=dict(t=70, b=20, l=20, r=20),
    legend_title="장르",
)

st.plotly_chart(
    fig_genre,
    use_container_width=True,
    config={"displayModeBar": False},
)


# -----------------------------
# 그래프 1 해석
# -----------------------------
st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 1 해석",
    placeholder="예: 가장 많은 영화가 속한 장르는 ○○이고, 전체 영화의 약 ○○%를 차지한다.",
    height=90,
    label_visibility="collapsed",
    key="interpretation_1",
)


st.divider()


# ============================================================
# 그래프 2. 장르 안에 들어 있는 영화
# ============================================================
st.header("2. 장르 안에 들어 있는 영화")

st.caption(
    "각 장르 안의 영화 크기는 총 관객 수에 비례합니다."
)

# 트리맵에 사용할 데이터
treemap_df = df[
    ["genre_first", "movieNm", "total_audi"]
].copy()

# 총 관객이 0인 데이터는 트리맵에서 제외
treemap_df = treemap_df[
    treemap_df["total_audi"] > 0
]

fig_treemap = px.treemap(
    treemap_df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르별 영화와 총 관객",
)

fig_treemap.update_traces(
    textinfo="label",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    ),
)

fig_treemap.update_layout(
    height=650,
    margin=dict(t=70, b=20, l=20, r=20),
)

st.plotly_chart(
    fig_treemap,
    use_container_width=True,
    config={"displayModeBar": False},
)


# -----------------------------
# 그래프 2 해석
# -----------------------------
st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 2 해석",
    placeholder="예: ○○ 장르에서는 ○○ 영화의 총 관객이 가장 많다.",
    height=90,
    label_visibility="collapsed",
    key="interpretation_2",
)


st.divider()


# ============================================================
# 원본 데이터
# ============================================================
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

    display_df["openDt"] = display_df["openDt"].dt.strftime(
        "%Y-%m-%d"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )
