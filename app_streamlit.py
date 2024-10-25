import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Toolbox tổng hợp số liệu")

uploaded_file = st.file_uploader("Chọn file dữ liệu CSV/Excel", type=["csv", "xlsx"])

cycle_option = st.selectbox("Chọn chu kỳ thời gian", ["30 phút", "1 giờ"])
summary_option = st.selectbox("Chọn kiểu tổng sản lượng", ["Theo ngày", "Theo tháng", "Theo quý", "Theo năm"])

output_filename = st.text_input("Nhập tên file để lưu (không cần phần mở rộng)", value="output")

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    df.set_index('Time', inplace=True)

    if cycle_option == "30 phút":
        df_resampled = df.resample('30T').mean()
    elif cycle_option == "1 giờ":
        df_resampled = df.resample('H').mean()

    if summary_option == "Theo ngày":
        df_summary = df_resampled.resample('D').sum()
    elif summary_option == "Theo tháng":
        df_summary = df_resampled.resample('M').sum()
    elif summary_option == "Theo quý":
        df_summary = df_resampled.resample('Q').sum()
    elif summary_option == "Theo năm":
        df_summary = df_resampled.resample('Y').sum()

    st.subheader("Biểu đồ dữ liệu tổng hợp")
    
    fig_line = px.line(df_summary, x=df_summary.index, y=df_summary.columns, title="Biểu đồ đường cho các khu vực")
    st.plotly_chart(fig_line)

    fig_bar = px.bar(df_summary, x=df_summary.index, y=df_summary.sum(axis=1), title="Tổng sản lượng theo thời gian", labels={'y': 'Tổng sản lượng', 'x': 'Thời gian'})
    st.plotly_chart(fig_bar)

    output_file = f"{output_filename}.xlsx"
    df_summary.to_excel(output_file)

    with open(output_file, 'rb') as f:
        st.download_button("Tải xuống file Excel", data=f, file_name=output_file)
