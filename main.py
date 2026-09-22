# ============================================================
# 그래프 2. 장르별 영화 관객수 트리맵
# ============================================================
st.header("2. 장르 안에 들어 있는 영화")

# total_audi 숫자형 변환
df["total_audi"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
).fillna(0)

# 트리맵용 데이터
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
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    ),
    textinfo="label",
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
# 그래프 해석 입력 영역
# -----------------------------
st.subheader("이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 정리해 보세요.",
    placeholder="예: ○○ 장르에는 총 관객이 많은 영화가 상대적으로 많이 포함되어 있다.",
    height=90,
    label_visibility="collapsed",
)

st.divider()
