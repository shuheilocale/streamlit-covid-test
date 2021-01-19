import streamlit as st
import json
import pandas as pd
import geopandas as gpd
import plotly.express as px



from read_patients_xlsx import read_patients_xlsx

# コロプレス図の中心
CENTER = {'lat': 36, 'lon': 140}

jpn = gpd.read_file('japan.geojson')
print(jpn)

#jpn.set_index('id', drop=False, inplace=True)

print(jpn)
df_patients = read_patients_xlsx('000721104.xlsx')
df_patients['capacity_rate'] = \
    df_patients['n_patients'] /  ( df_patients['capacity_hospital'] + df_patients['capacity_inn'] )


df_jpn = pd.merge(jpn, df_patients, on='id', how='left')
df_jpn.set_index('id', drop=False, inplace=True)
print(df_jpn)


# colorを変更することで都道府県ごとに色を決定できる。
fig = px.choropleth_mapbox(df_jpn, geojson=json.loads(df_jpn['geometry'].to_json()), 
    locations='id', 
    color='capacity_rate',
    title = 'コロナ患者の病床キャパシティ',
    hover_name = 'nam_ja',
    color_continuous_scale=[(0, "cornsilk"), (0.5, "red"), (1, "black")], 
    range_color=[0,1],
    mapbox_style='white-bg',
    zoom=4, 
    center=CENTER,
    opacity=0.5,
    labels={'capacity_rate':'キャパシティ'}
    )


fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={'r':10,'t':40,'l':10,'b':10,'pad':5})
#fig.show()
st.plotly_chart(fig)