import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 


st.set_page_config(page_title = "Movies analysis")
st.header("DASHBOARD PHÂN TÍCH DỮ LIỆU")
st.write("#### Thành viên:")
st.write("- Hà Đức Phú - 2321050006")
st.write("- Trần Ngọc Minh - 2321050016")

movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/Dataset%20for%20Practice/movies.csv")

df_cleaned = movies_data.dropna(subset=['genre'])

year_list = movies_data['year'].unique().tolist()

st.write("5 dòng đầu của bảng dữ liệu")
st.dataframe(movies_data.head())

st.write("5 dòng cuối của bảng dữ liệu")
st.dataframe(movies_data.tail())


st.sidebar.subheader("Bảng dữ liệu của các bộ phim lẻ 1980-2020:")
st.sidebar.dataframe(movies_data)

genre_counts = df_cleaned['genre'].str.split('|', expand=True).stack().value_counts()


plt.figure(figsize=(10, 6))
plt.bar(genre_counts.index, genre_counts.values)
plt.xlabel('Thể loại')
plt.ylabel('Số lượng phim')
plt.title('Số lượng phim theo thể loại')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(plt)

plt.figure(figsize=(10, 6))
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()
the_loai = avg_budget['genre']
kinh_phi_tb = avg_budget['budget']
plt.bar(the_loai, kinh_phi_tb, color = 'coral')
plt.xlabel('Thể loại')
plt.ylabel('Kinh phí')
plt.title('Biểu đồ thể hiện ngân sách trung bình của các bộ phim thuộc các thể loại khác nhau')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(plt)

#web: http://localhost:8501/