import streamlit as st
import pandas as pd
import os
from io import BytesIO

# 🎨 Configure the Streamlit app's appearance and layout
st.set_page_config(page_title="🚀 Data Sweeper", layout="wide")

# 🏆 Display the main app title and introductory text
st.title("🧹 Advanced Data Sweeper")
st.write("🚀 **Convert & Clean Your Data!** Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# 📤 File uploader widget (supports multiple CSV & Excel files)
uploaded_files = st.file_uploader("📂 **Upload your files (CSV or Excel):**", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()

        # 🧐 Read file based on extension
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.error(f"❌ Unsupported file type: {file_extension}")
            continue

        # 🔍 File details
        st.write(f"📄 **File Name:** `{file.name}`")
        st.write(f"📏 **File Size:** `{file.size / 1024:.2f} KB`")

        # 👀 Preview uploaded file
        st.subheader("🔍 File Preview:")
        st.dataframe(df.head())

        # 🛠️ Data cleaning options
        st.subheader("🛠️ Data Cleaning")
        if st.checkbox(f"🧼 Clean Data for `{file.name}`"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🚫 Remove Duplicates - {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ **Duplicates Removed!**")
            with col2:
                if st.button(f"📊 Fill Missing Values - {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ **Missing Values Filled with Column Means!**")

        # 🎯 Column selection
        st.subheader("🎯 Select Columns to Keep")
        columns = st.multiselect(f"📝 Choose Columns - `{file.name}`", df.columns, default=df.columns)
        df = df[columns]

        # 📊 Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📈 Show Visualization for `{file.name}`"):
            numeric_cols = df.select_dtypes(include=['number'])
            if not numeric_cols.empty:
                st.bar_chart(numeric_cols.iloc[:, :2])
            else:
                st.warning("⚠️ No numeric columns available for visualization.")

        # 🔄 File Conversion Options
        st.subheader("🔄 Convert & Download")
        conversion_type = st.radio(f"🔁 Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"🔄 Convert `{file.name}`"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # ⬇️ Download button
            st.download_button(
                label=f"⬇️ Download `{file.name}` as `{conversion_type}`",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 **All files processed successfully!** 🚀")
