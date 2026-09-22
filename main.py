# ============================================================
# 그래프 4. 개봉일 스크린 수와 총 관객의 관계
# ============================================================
st.header("4. 개봉일 스크린 수와 총 관객의 관계")

scatter_df = df[
    ["movieNm", "genre_first", "first_scrn", "total_audi"]
].copy()

# 숫자형으로 변환
scatter_df["first_scrn"] = pd.to_numeric(
    scatter_df["first_scrn"],
    errors="coerce",
)

scatter_df["total_audi"] = pd.to_numeric(
    scatter_df["total_audi"],
    errors="coerce",
)

# 필요한 값이 없는 행 제거
scatter_df = scatter_df.dropna(
    subset=["first_scrn", "total_audi"]
)

# 스크린 수와 관객 수가 0보다 큰 영화만 사용
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


# -----------------------------
# 그래프 4 해석
# -----------------------------
st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 4 해석",
    placeholder="예: 개봉일 스크린 수가 많은 영화일수록 총 관객도 많은 경향이 나타난다.",
    height=90,
    label_visibility="collapsed",
    key="interpretation_4",
)

st.divider()
