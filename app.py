import streamlit as st
import pandas as pd

# GoogleスプレッドシートID
SHEET_ID = "11w79e7fpomMbMTfpsXf0o350TCxSagKDVozto6h_mdk"

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# シーン一覧
scenes = {
    "プロローグ": {"25齋藤", "26奥村", "24浅野"},
    "シーン1": {"24下川", "24浅野", "26水野"},
    "シーン2": {"24下川", "25高橋", "24浅野"},
    "シーン3": {"24下川", "24浅野", "25安孫子", "26水野", "26神保"},
    "シーン4前": {"24下川", "24浅野"},
    "シーン4中": {"25安孫子", "25高橋", "25齋藤", "26神保", "26奥村", "26成瀬"},
    "シーン4後": {"24下川", "25高橋"},
    "シーン5": {"26神保", "26水野", "24下川", "25安孫子"},
    "シーン6": {"25齋藤", "26奥村", "26成瀬"},
    "シーン7": {"26水野", "25高橋"},
    "シーン8": {"24下川", "24浅野", "25高橋"},
    "シーン10": {"25齋藤", "26成瀬", "26奥村"},
    "シーン11": {"24下川", "24浅野", "25安孫子", "25高橋", "26神保", "26水野"},
    "シーン12": {"25安孫子", "26神保", "24下川"},
    "シーン13前": {"24下川", "24浅野", "25齋藤"},
    "シーン13後": {"24浅野", "25安孫子", "25高橋", "25齋藤", "26神保", "26水野", "26成瀬"},
    "シーン14": {"24下川", "25安孫子", "25高橋", "26神保", "26水野"}
}

st.set_page_config(page_title="カシオレ シーン判定", layout="wide")

st.title("カシオレ シーン判定")

st.write("ボタンを押すと最新の出席状況を読み込みます。")

if st.button("シーンを表示"):

    df = pd.read_csv(url, header=2)

    # 空の列を削除
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # 日付セル結合対策
    df.iloc[:, 0] = df.iloc[:, 0].ffill()

    members = df.columns[2:]

    for _, row in df.iterrows():

        date = row.iloc[0]

        attendance = set()

        for person in members:

            mark = str(row[person]).strip()

            if mark == "◯":
                attendance.add(person)

        available = []
        almost = []

        for scene, need in scenes.items():

            if need.issubset(attendance):

                available.append(scene)

            else:

                missing = need - attendance

                if len(missing) == 1:
                    almost.append((scene, list(missing)[0]))

        st.divider()

        st.header(f"{date}")

        st.subheader("できるシーン")

        if available:

            for scene in available:
                st.write(f"・{scene}")

        else:

            st.write("できるシーンはありません")

        st.subheader("あと1人でできるシーン")

        if almost:

            for scene, person in almost:
                st.write(f"・{scene}（あと **{person}**）")

        else:

            st.write("ありません")
