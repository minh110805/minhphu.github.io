import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================
# 1. Tải & đổi tên cột sang tiếng Việt
# ============================
@st.cache_data
def load_data():
    df = pd.read_csv("Amazon-Products-clean.csv")

    # Đổi tên cột sang tiếng Việt
    rename_map = {
        "name": "tên_sản_phẩm",
        "main_category": "danh_mục",
        "sub_category": "danh_mục_con",
        "ratings": "điểm_đánh_giá",
        "no_of_ratings": "số_lượng_đánh_giá",
        "discount_price": "giá_khuyến_mãi",
        "actual_price": "giá_gốc",
    }
    df = df.rename(columns=rename_map)

    # Làm sạch giá
    df["giá_khuyến_mãi"] = (
        df["giá_khuyến_mãi"]
        .astype(str).str.replace("$", "").str.replace(",", "")
        .astype(float)
    )

    # Làm sạch điểm đánh giá
    df["điểm_đánh_giá"] = (
        df["điểm_đánh_giá"]
        .astype(str)
        .str.extract(r"(\d+(\.\d+)?)")[0]
        .astype(float)
    )

    return df

df = load_data()

# ============================
# 2. Tiêu đề ứng dụng
# ============================
st.title("📊 Dashboard Sản phẩm Amazon")

# ============================
# 3. Sidebar lọc dữ liệu
# ============================
st.sidebar.header("Bộ lọc")

selected_category = st.sidebar.selectbox(
    "Chọn danh mục",
    ["Tất cả"] + sorted(df["danh_mục"].dropna().unique().tolist())
)
min_price, max_price = st.sidebar.slider(
    "Khoảng giá (USD)",
    float(df["giá_khuyến_mãi"].min()),
    float(df["giá_khuyến_mãi"].max()),
    (float(df["giá_khuyến_mãi"].min()), float(df["giá_khuyến_mãi"].max()))
)

# Áp dụng bộ lọc
filtered_df = df.copy()
if selected_category != "Tất cả":
    filtered_df = filtered_df[filtered_df["danh_mục"] == selected_category]

filtered_df = filtered_df[
    (filtered_df["giá_khuyến_mãi"] >= min_price) &
    (filtered_df["giá_khuyến_mãi"] <= max_price)
]

# Bảng dữ liệu
if st.checkbox("Hiển thị bảng dữ liệu"):
    st.write(filtered_df.head(50))

# ============================
# 4. Biểu đồ: Phân bố giá
# ============================
st.subheader("📌 Phân bố giá sản phẩm")

fig1, ax1 = plt.subplots()
ax1.hist(filtered_df["giá_khuyến_mãi"].dropna(), bins=40)
ax1.set_xlabel("Giá (USD)")
ax1.set_ylabel("Số lượng sản phẩm")
st.pyplot(fig1)

# ============================
# 5. Biểu đồ: Giá vs Điểm đánh giá
# ============================
st.subheader("📈 Mối quan hệ giữa Giá và Điểm đánh giá")

fig2, ax2 = plt.subplots()
ax2.scatter(filtered_df["giá_khuyến_mãi"], filtered_df["điểm_đánh_giá"], s=10, alpha=0.5)
ax2.set_xlabel("Giá (USD)")
ax2.set_ylabel("Điểm đánh giá (0–5)")
ax2.set_ylim(0, 5.1)
st.pyplot(fig2)

# ============================
# 6. Top danh mục nhiều sản phẩm nhất
# ============================
st.subheader("🏷️ Top danh mục nhiều sản phẩm nhất")

top_cat = df["danh_mục"].value_counts().head(15)

fig3, ax3 = plt.subplots()
ax3.barh(top_cat.index[::-1], top_cat.values[::-1])
ax3.set_xlabel("Số lượng sản phẩm")
st.pyplot(fig3)

# ============================
# 7. Điểm đánh giá trung bình theo danh mục
# ============================
st.subheader("⭐ Điểm đánh giá trung bình theo danh mục")

avg_rating = df.groupby("danh_mục")["điểm_đánh_giá"].mean().dropna().sort_values(ascending=False).head(15)

fig4, ax4 = plt.subplots()
ax4.barh(avg_rating.index[::-1], avg_rating.values[::-1])
ax4.set_xlabel("Điểm trung bình")
st.pyplot(fig4)
