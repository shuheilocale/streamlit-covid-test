import os
import re

import streamlit as st
from PIL import Image
import easyocr
import pandas as pd

from monster import MonsterFactory, EncountMonsters



def judge(monster_nos, monster_factory):
    encount_monsters = EncountMonsters(monster_factory, monster_nos)
    msg = encount_monsters.judge_mass()
    return {
        'df': encount_monsters.to_df(),
        'msg': msg
    }

def extract_numbers(text):
    pattern = r'N[oO0][,.]?(\d+)'
    matches = re.findall(pattern, text)
    return matches


def main(reader):

    # 外部で保持する値
    if st.button('ほげ'):
        st.session_state['monster_1'] = 122


    st.title('宝の地図大量発生判定')
    st.write('出現モンスターの図鑑No.を入力してください。')

    df = pd.read_csv('monster_list.csv')
    monster_factory = MonsterFactory(df)

    uploaded_files = st.file_uploader('スクショアップロード', accept_multiple_files=True, type=['jpg','jpeg','png'])

    if uploaded_files is not None:
        monster_nos = []

        for upload_file in uploaded_files:

            pil = Image.open(upload_file)
            results = reader.readtext(pil)

            for result in results:
                monster_nos += extract_numbers(result[1])


        monster_nos = list(set(monster_nos))[:12]

        for i, monster_no in enumerate(monster_nos):
            st.session_state[f'monster_{i+1}'] = monster_no


    monster_nos = []
    for i in range(12):
        col1, col2 = st.columns([1, 2])
        with col1:

            number = st.number_input(f'モンスター{i+1}', value=0, key=f'monster_{i+1}')
            monster_nos.append(number)
        with col2:
            try:
                monster = monster_factory.create_monster_by_no(number)
                name = f'{monster.name}（{monster.findability.short_str()},{monster.exp_ratio.value}）'
            except:
                name = ''
            col2.markdown("##")
            col2.markdown(name)


    if st.button('判定'):

        try:
            result = judge(monster_nos
                # 29,74,121,159,161,166,222,277,326,336,455,520
            , monster_factory)

            st.subheader(result['msg'])

            st.table(result['df'])
        except Exception as e:
            st.error(e)



    st.markdown('''
    #### 参考元
- 判定ロジック
  - すずしろ店長様
  - https://twitter.com/Lv20_HP140MP80/status/1709521858377466185
- データソース
  - すずしろ店長様
  - https://docs.google.com/spreadsheets/d/1Hz-v2lBDV5khxgFRMZAhBDWqn65Inv3vjD2NpS8FwsM/edit#gid=1463845531''')




if __name__ == '__main__':

    reader = easyocr.Reader(['ja','en'],gpu = False)
    main(reader)
