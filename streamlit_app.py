import json
import geopandas as gpd
import plotly.express as px

# コロプレス図の中心
CENTER = {'lat': 36, 'lon': 140}

jpn = gpd.read_file('japan.geojson')
print(jpn)

jpn.set_index('id', drop=False, inplace=True)


# colorを変更することで都道府県ごとに色を決定できる。
fig = px.choropleth_mapbox(jpn, geojson=json.loads(jpn['geometry'].to_json()), 
    locations='id', 
    color='id',
    title = '人口密度',
    hover_name = 'nam_ja',
    color_continuous_scale="OrRd", 
    mapbox_style='white-bg',
    zoom=4, 
    center=CENTER,
    opacity=0.5,
    labels={'DENSITY':'人口密度'}
    )
fig.update_layout(margin={'r':10,'t':40,'l':10,'b':10,'pad':5})
fig.show()