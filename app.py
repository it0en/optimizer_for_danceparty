import streamlit as st
import pandas as pd
import random

st.title("ショーケース最適順計算アプリ")
st.write("Excelファイルをアップロードして、早替えが最小になるショーケース順を求めます。")

uploaded_file = st.file_uploader("Excelファイルをアップロード", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    all_data = []
    for col in df.columns[1:]:  # 1列目は無視
        members = df[col].dropna().tolist()
        if members:
            all_data.append((col, members))

    if not all_data:
        st.error("ショーケースが見つかりません。2列目以降にショーケースを配置してください。")
    else:
        data_num = len(all_data)
        decision = data_num
        decision_data = []

        for k in range(1000):
            random.shuffle(all_data)
            con = [0 for _ in range(data_num)]

            for i in range(data_num - 1):
                set1 = set(all_data[i][1])
                set2 = set(all_data[i + 1][1])
                if set1 & set2:
                    con[i + 1] = 1

            tmp = sum(con)
            if tmp < decision:
                decision = tmp
                decision_data = list(all_data)
                if decision == 0:
                    break

        st.success(f"早替え数: {decision}")
        st.subheader("最適コマ順:")
        for i, (showcase_name, members) in enumerate(decision_data):
            st.markdown(f"**{i+1}. {showcase_name}**: {', '.join(map(str, members))}")
