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

    # 숫자형 데이터 변환
    df["first_scrn"] = pd.to_numeric(
        df["first_scrn"],
        errors="coerce",
    )

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
st.caption(
    "1년간 박스오피스 10위권에 든 영화 데이터를 그래프로 살펴봅니다."
)

st.write(
    f"전체 영화 **{len(df):,}편**을 대상으로 "
    "장르와 관객 분포를 살펴봅니다."
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

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 1 해석",
    placeholder=(
        "예: 가장 많은 영화가 속한 장르는 ○○이고, "
        "전체 영화의 약 ○○%를 차지한다."
    ),
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

treemap_df = df[
    ["genre_first", "movieNm", "total_audi"]
].copy()

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

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 2 해석",
    placeholder=(
        "예: ○○ 장르에서는 ○○ 영화의 총 관객이 "
        "가장 많다."
    ),
    height=90,
    label_visibility="collapsed",
    key="interpretation_2",
)

st.divider()


# ============================================================
# 그래프 3. 총 관객 히스토그램
# ============================================================
st.header("3. 영화별 총 관객 분포")

hist_df = df[
    df["total_audi"] > 0
].copy()

fig_hist = px.histogram(
    hist_df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객(명)",
        "count": "영화 편수",
    },
)

fig_hist.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    ),
)

fig_hist.update_layout(
    height=500,
    xaxis_title="총 관객(명)",
    yaxis_title="영화 편수",
    margin=dict(t=70, b=50, l=50, r=20),
)

st.plotly_chart(
    fig_hist,
    use_container_width=True,
    config={"displayModeBar": False},
)


# -----------------------------
# 가장 많은 영화가 몰린 구간 계산
# -----------------------------
hist_bins = pd.cut(
    hist_df["total_audi"],
    bins=20,
)

bin_counts = (
    hist_bins
    .value_counts()
    .sort_index()
)

most_common_bin = bin_counts.idxmax()

bin_start = most_common_bin.left
bin_end = most_common_bin.right


# -----------------------------
# 가장 관객이 많은 영화 찾기
# -----------------------------
max_audience_row = df.loc[
    df["total_audi"].idxmax()
]

max_movie_name = max_audience_row["movieNm"]
max_audience = int(max_audience_row["total_audi"])


st.subheader("이 그래프로 알 수 있는 것")

st.markdown(
    f"""
- **대부분의 영화가 몰려 있는 구간:** 약
  **{bin_start:,.0f}명 ~ {bin_end:,.0f}명**
  구간에 영화가 가장 많이 몰려 있습니다.
- **가장 관객이 많은 영화:** **{max_movie_name}**
  — 총 **{max_audience:,}명**입니다.
"""
)

st.divider()


# ============================================================
# 그래프 4. 개봉일 스크린 수와 총 관객의 관계
# ============================================================
st.header("4. 개봉일 스크린 수와 총 관객의 관계")

scatter_df = df[
    ["movieNm", "genre_first", "first_scrn", "total_audi"]
].copy()

scatter_df = scatter_df.dropna(
    subset=["first_scrn", "total_audi"]
)

scatter_df = scatter_df[
    (scatter_df["first_scrn"] > 0)
    & (scatter_df["total_audi"] > 0)
]

fig_scatter = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객",
        "genre_first": "장르",
    },
    title="개봉일 스크린 수와 총 관객",
)

fig_scatter.update_traces(
    marker=dict(
        size=9,
        opacity=0.7,
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,}개<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    ),
)

fig_scatter.update_layout(
    height=600,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객",
    margin=dict(t=70, b=50, l=60, r=20),
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True,
    config={"displayModeBar": False},
)

st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 4 해석",
    placeholder=(
        "예: 개봉일 스크린 수와 총 관객 사이에는 "
        "어떤 관계가 나타나는지 살펴볼 수 있다."
    ),
    height=90,
    label_visibility="collapsed",
    key="interpretation_4",
)

st.divider()


# ============================================================
# 그래프 5. 장르별 총 관객 상자 그림
# ============================================================
st.header("5. 장르별 총 관객 분포")

st.caption(
    "영화가 10편 이상인 장르만 골라 총 관객 분포를 비교합니다."
)


# 영화가 10편 이상인 장르 찾기
genre_movie_counts = (
    df["genre_first"]
    .value_counts()
)

eligible_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index


# 조건에 맞는 영화만 추출
boxplot_df = df[
    df["genre_first"].isin(eligible_genres)
    & (df["total_audi"] > 0)
].copy()


# 영화명을 customdata로 넣기 위해 별도 컬럼 사용
fig_box = px.box(
    boxplot_df,
    x="genre_first",
    y="total_audi",
    color="genre_first",
    points="outliers",
    custom_data=["movieNm"],
    labels={
        "genre_first": "장르",
        "total_audi": "총 관객",
    },
    title="영화가 10편 이상인 장르의 총 관객 분포",
)


# 이상치에 마우스를 올렸을 때 영화명 표시
fig_box.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "장르: %{x}<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    ),
)


fig_box.update_layout(
    height=600,
    showlegend=False,
    xaxis_title="장르",
    yaxis_title="총 관객",
    margin=dict(t=70, b=50, l=60, r=20),
)


st.plotly_chart(
    fig_box,
    use_container_width=True,
    config={"displayModeBar": False},
)


st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 5 해석",
    placeholder=(
        "예: 장르별 총 관객의 중앙값과 분포의 차이를 비교할 수 있다."
    ),
    height=90,
    label_visibility="collapsed",
    key="interpretation_5",
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
