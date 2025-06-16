import streamlit as st
import pandas as pd

st.title("コマ組み文字起こしアプリ")
st.write("Excelファイルをアップロードして、コマ組みを文字起こしします。")

uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx"])

if uploaded_file:
    # シート名一覧の取得
    excel_file = pd.ExcelFile(uploaded_file)
    sheet_name = st.selectbox("シートを選択してください", excel_file.sheet_names)

    if sheet_name:
        # データの読み込み
        data = pd.read_excel(excel_file, sheet_name=sheet_name, header=None, skiprows=1)

        formatted_text = []

        def delete_number(a):
            while a != "":
                if a[-1].isdecimal() or a[-1] == ".":
                    a = a[:-1]
                else:
                    break
            return a

        pre_location = ""
        for index, row in data.iterrows():
            flag = 0
            time_info = row[0]
            location = row[1] if pd.notna(row[1]) else ''
            activity1 = row[2] if pd.notna(row[2]) else ''
            activity2 = row[3] if pd.notna(row[3]) else ''
            activity1 = delete_number(activity1)
            activity2 = delete_number(activity2)

            if pd.notna(time_info):
                time_info = str(time_info)
                if time_info[-1] == ")":
                    formatted_text.append("")
                    formatted_text.append(time_info)
                    flag = 1
                    continue

            if (str(location) != "" and (location != pre_location)) or flag == 1:
                formatted_text.append(f"@{location}")
                flag = 0

            if pd.notna(time_info) and (activity1 or activity2):
                if activity1 and activity2:
                    formatted_text.append(f"{time_info} {activity1}/{activity2}")
                elif activity1:
                    formatted_text.append(f"{time_info} {activity1}")
                elif activity2:
                    formatted_text.append(f"{time_info} {activity2}")
            elif pd.notna(time_info):
                formatted_text.append(f"{time_info}")

            pre_location = location

        formatted_output = "\n".join([line for line in formatted_text if "施設なし" not in line])

        st.subheader("フォーマット結果")
        st.text(formatted_output)
