df = pd.read_excel("../original_data/private_institute.xlsx")
df_code = pd.read_excel("../original_data/district_code_seoul.xlsx")
df_land = pd.read_csv("../original_data/land_price.csv", engine = 'python')

df_code = df_code.rename(columns = {'통계청행정동코드' : 'code', '행자부행정동코드':'code_mois', '시도명':'city', '시군구명':'district', '행정동명': 'village'})
df_code = df_code.drop([0])
df_code["code"] = df_code["code"].astype('str')
df_code["code_district"] = df_code["code"].str[0:5]
df_code = df_code.drop_duplicates(['district'])
df_code = df_code.drop(['city','village', 'code', 'code_mois'], axis = 1)

df =df[['district', 'university related institute']]
df = df.drop([0])

df = pd.merge(df, df_code, how = "left")

state_geo = '../original_data/skorea_municipalities_geo_simple.json'

with open(state_geo, encoding='utf-8') as f:
    json_data = json.load(f)

#Error solution: jupyter notebook --NotebookApp.iopub_data_rate_limit=1.0e10

df_land = df_land.rename(columns = {'시군구명': 'district', '필지구분명': 'land_type',  '공시지가(원/㎡)':'land_price'})
df_land = df_land[df_land["land_type"]=="토지"]
df_price = pd.DataFrame(df_land.groupby("district")["land_price"].mean()).reset_index()
df_price = pd.merge(df, df_land, how = "left")

map_institute = folium.Map(location=[37.564214, 127.001699], tiles="OpenStreetMap", zoom_start=11)
#stamentoner

map_institute.choropleth(
    geo_data=json_data,
    data=df,
    columns=['district', 'university related institute'],
    fill_color='Blues',
    fill_opacity=0.7,
    line_opacity=0.3,
    color = 'gray',
    key_on = 'feature.id'
)

map_houseprice = folium.Map(location=[37.564214, 127.001699], tiles="OpenStreetMap", zoom_start=11)
#stamentoner

map_houseprice.choropleth(
    geo_data=json_data,
    data=df_price,
    columns=["district", "land_price"],
    fill_color='PuRd',
    fill_opacity=0.7,
    line_opacity=0.3,
    color = 'gray',
    key_on = 'feature.id'
)

