import streamlit as st
import pandas as pd
import plotly.express as px
def app():
    st.header("서울시 소방대상물 위치정보")
    data=pd.read_csv('data/위치정보_data.csv',encoding='cp949')
    data["건물층수"]=data["건물층수"].apply(lambda x:int(x))
    data=data.head(1000)
    col_filter1, col_filter2, col_filter3, col_filter4 = st.beta_columns(4)
    del col_filter2, col_filter3, col_filter4
    temp_list=sorted(data["건물층수"].tolist())
    temp=tuple(set(temp_list))
    t=('전체',)+temp
    st_side_filter = col_filter1.selectbox("건물층수를 선택하세요", t)
    col1,col2,col3,col4=st.beta_columns(4)
    if col1.checkbox("지도 보기",value=True):
        if st_side_filter == "전체":
            fig=px.scatter_mapbox(data,lat="위도",lon="경도",color="건물층수",size="건물층수",hover_name="대상물이름",hover_data=["건물층수"], color_discrete_sequence=px.colors.cyclical.IceFire,zoom=13)
        else:
            data=data[data["건물층수"]==st_side_filter]
            fig = px.scatter_mapbox(data, lat="위도", lon="경도", color="건물층수", size="건물층수", hover_name="대상물이름",
                                    hover_data=["건물층수"], color_discrete_sequence=px.colors.cyclical.IceFire, zoom=13)
        fig.update_layout(mapbox_style="open-street-map",height=800)
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig,use_container_width=True)
        #####################