# -----------------------------
# 히스토그램에서 가장 많은 구간 찾기
# -----------------------------
hist_counts, bin_edges = np.histogram(
    hist_df["total_audi"],
    bins=20,
)

max_bin_index = hist_counts.argmax()

bin_start = bin_edges[max_bin_index]
bin_end = bin_edges[max_bin_index + 1]

# 가장 관객이 많은 영화 찾기
max_audience_row = df.loc[
    df["total_audi"].idxmax()
]

max_movie_name = max_audience_row["movieNm"]
max_audience = int(max_audience_row["total_audi"])


# -----------------------------
# 그래프 아래 설명 문구
# -----------------------------
st.subheader("이 그래프로 알 수 있는 것")

st.markdown(
    f"""
- **대부분의 영화가 몰려 있는 구간:** 약 **{bin_start:,.0f}명 ~ {bin_end:,.0f}명** 구간에 영화가 가장 많이 몰려 있습니다.
- **가장 관객이 많은 영화:** **{max_movie_name}** — 총 **{max_audience:,}명**입니다.
"""
)
