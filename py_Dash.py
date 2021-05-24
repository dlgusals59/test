import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit import caching

def app():
    caching.clear_cache()
    ###################################data LOADING############################
    data=pd.read_csv('data/calender_data.csv',thousands = ',')
    month_data=pd.read_csv('data/month_data.csv',thousands = ',')
    discount_data=pd.read_csv('data/discount.csv',thousands = ',')
    product_data=pd.read_csv('data/품목분류_data.csv',thousands = ',')
    product_data_qty=pd.read_csv('data/품목분류_data_수량.csv',thousands = ',')
    ###########################################################################
    ###############
    ###########################################################################
    st.title('판매 분석 대시보드')
    col_filter1, col_filter2, col_filter3, col_filter4 = st.beta_columns(4)
    del col_filter2, col_filter3, col_filter4
    st_side_filter = col_filter1.selectbox("년도를 선택하세요", ("전체", 2021, 2020,2019))
    if st_side_filter=="전체":
        fig = go.Figure()
        #총판매금액
        kpi_sum=round(data["판매금액"].sum()/1000)
        fig.add_trace(go.Indicator(
            number={'valueformat': ',', 'font': {'size': 30}},
            mode="number",
            value=kpi_sum,
            domain={'row': 0, 'column': 0},
            title={'text': '<b>'+"총 판매금액(단위:천 원)"+'</b>', 'font': {'size': 17}}))

        #작년대비증감률
        data_2021 = data[data["거래년도"] == 2021]
        s_2021 = data_2021["판매금액"].sum()
        x_2021 = round(s_2021 / 1000)
        ##################
        data_2020 = data[data["거래년도"] == 2020]
        s_2020 = data_2020["판매금액"].sum()
        x_2020 = round(s_2020 / 1000)
        x_incdec = round((s_2021 / s_2020 - 1) * 100, 1)
        fig.add_trace(go.Indicator(
            number={'valueformat': '.1%', 'font': {'size': 30}},
            mode="number",
            value=x_incdec / 100,
            domain={'row': 0, 'column': 1},
            title={'text': '<b>'+"2021년 기준 작년 대비 증감률"+'</b>', 'font': {'size': 17}}))
        #전체 수익 금액
        discount_sum=round(discount_data["수익금액"].sum()/1000)
        fig.add_trace(go.Indicator(
            number={'valueformat': ',', 'font': {'size': 30}},
            mode="number",
            value=discount_sum,
            domain={'row': 0, 'column': 2},
            title={'text': '<b>'+"전체 수익 금액(단위:천 원)"+'</b>', 'font': {'size': 17}}))
        #전체 할인율
        discount_rate = round(discount_data["할인율"].sum()/3,4)
        fig.add_trace(go.Indicator(
            number={'valueformat': '.2%', 'font': {'size': 30}},
            mode="number",
            value=discount_rate,
            domain={'row': 0, 'column': 3},
            title={'text': '<b>'+"전체 할인율(%)"+'</b>', 'font': {'size': 17}}))
        fig.update_layout(
            grid={'rows': 1, 'columns': 4, 'pattern': "independent"},
            autosize=True,
            font={'color': "darkblue", 'family': "Balto"},
            height=100
        )
        st.plotly_chart(fig, use_container_width=True)
        #############################
    else:
        discount_data = discount_data[discount_data["거래년도"] == st_side_filter]
        data_dec = data[data["거래년도"] == st_side_filter-1]
        data = data[data["거래년도"] == st_side_filter]
        month_data = month_data[month_data["거래년도"] == st_side_filter]
        product_data = product_data[product_data["거래년도"] == st_side_filter]
        product_data_qty = product_data_qty[product_data_qty["거래년도"] == st_side_filter]
        fig = go.Figure()
        # 총판매금액
        kpi_sum =round(data["판매금액"].sum()/1000)
        fig.add_trace(go.Indicator(
            number={'valueformat': ',', 'font': {'size': 30}},
            mode="number",
            value=kpi_sum,
            domain={'row': 0, 'column': 0},
            title={'text': '<b>'+str(st_side_filter)+"년 총 판매금액(단위: 천원)"+'</b>', 'font': {'size': 17}}))
        # 작년대비증감률
        if st_side_filter==2019:
            fig.add_trace(go.Indicator(
                number={'valueformat': '.1%', 'font': {'size': 30}},
                mode="number",
                value=0,
                domain={'row': 0, 'column': 1},
                title={'text': '<b>'+str(st_side_filter) + "년 기준 작년 대비 증감률"+'</b>', 'font': {'size': 17}}))
        else:
            x_incdec=(data["판매금액"].sum()/data_dec["판매금액"].sum())-1
            x_incdec=round((x_incdec) * 100, 1)
            fig.add_trace(go.Indicator(
                number={'valueformat': '.1%', 'font': {'size': 30}},
                mode="number",
                value=x_incdec / 100,
                domain={'row': 0, 'column': 1},
                title={'text': '<b>'+str(st_side_filter)+"년 기준 작년 대비 증감률"+'</b>', 'font': {'size': 17}}))
        # 전체 할인 금액
        discount_sum = round(discount_data["수익금액"].sum() / 1000)
        fig.add_trace(go.Indicator(
            number={'valueformat': ',', 'font': {'size': 30}},
            mode="number",
            value=discount_sum,
            domain={'row': 0, 'column': 2},
            title={'text': '<b>'+str(st_side_filter)+"년 수익 금액(단위:천 원)"+'</b>', 'font': {'size': 17}}))
        # 전체 할인율
        discount_rate = round(discount_data["할인율"].sum(), 4)
        fig.add_trace(go.Indicator(
            number={'valueformat': '.2%', 'font': {'size': 30}},
            mode="number",
            value=discount_rate,
            domain={'row': 0, 'column': 3},
            title={'text': '<b>'+str(st_side_filter)+"년 할인율(%)"+'</b>', 'font': {'size': 17}}))
        fig.update_layout(
            grid={'rows': 1, 'columns': 4, 'pattern': "independent"},
            autosize=True,
            font={'color': "darkblue", 'family': "Balto"},
            height=100
        )
        st.plotly_chart(fig, use_container_width=True)
    ##################################################################
    col1, col2 = st.beta_columns(2)
    col3, col4 = st.beta_columns(2)
    month_data["판매금액"] = round(month_data["판매금액"] / 1000000)
    product_data["판매금액"] = pd.to_numeric(product_data["판매금액"])
    pie_sum = product_data.groupby(product_data["품목분류"], as_index=False)["판매금액"].sum()
    pie_sum=pie_sum.drop([0])
    piepull = [0.05 for i in range(len(product_data["품목분류"]))]
    fi = go.Figure(go.Pie(name='',labels=pie_sum["품목분류"], values=pie_sum["판매금액"]/1000000, pull=piepull,hole=0.1,text=pie_sum["판매금액"].apply(lambda x:"{:,}".format(int(round(x/1000000)))),
                          hovertemplate="품목분류=%{label} <br>판매비중(%)=%{percent} </br>판매금액(단위:백 만원)=%{text}"))
    #fi = px.pie(pie_sum, values=pie_sum["판매금액"], names=pie_sum["품목분류"], labels={"품목분류": "품목분류", "판매금액": "판매금액"},hole=0.2)
    fi.update_traces(textposition='inside', textinfo='percent+label')

    fi.update_layout(autosize=True)
    if st_side_filter=="전체":
        col1.subheader("전체 품목분류 판매금액 비율(단위:백만 원)")
    else:
        col1.subheader(str(st_side_filter)+"년 품목분류 판매금액 비율(단위:백만 원)")
    col1.plotly_chart(fi, use_container_width=True)
    ###################################
    pivot = pd.pivot_table(product_data, index='품목분류', columns=['거래년도'], values='판매금액').reset_index().fillna(0)
    #null 값 제거
    pivot=pivot.drop([0])

    if st_side_filter=="전체":
        pivot = pivot.sort_values(by=[2021], axis=0, ascending=False)
        pivot[2019] = round(pivot[2019] / 1000000)
        pivot[2020] = round(pivot[2020] / 1000000)
        pivot[2021] = round(pivot[2021] / 1000000)
        fig = px.bar(pivot, x="품목분류", y=[2019, 2020, 2021], barmode='group',
                    labels={"품목분류": "품목분류", "variable": "거래년도", "value": "판매금액(단위:백 만원)"}, text="value")
    else:
        pivot = pivot.sort_values(by=[st_side_filter], axis=0, ascending=False)
        pivot[st_side_filter]=round(pivot[st_side_filter]/1000000)
        pivot=pivot.rename(columns={st_side_filter : '판매금액'})
        fig = px.bar(pivot, x="품목분류", y="판매금액",labels={"품목분류": "품목분류", "판매금액":"판매금액(단위:백 만원)"}, text="판매금액",color = "품목분류",color_discrete_sequence = px.colors.qualitative.G10)
    for data in fig.data:
        data["width"] = 0.3
    fig.update_layout(autosize=True, plot_bgcolor="white", yaxis=dict(tickformat=","))
    #fig.update_layout(hovermode="x")
    fig.update_traces(textposition='outside')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='LightPink', gridwidth=1)
    if st_side_filter=="전체":
        col2.subheader("년도별 품목 중분류별 판매금액(단위:백 만원)")
    else:
        col2.subheader(str(st_side_filter) + " 년 품목 중분류별 판매금액(단위:백 만원)")
    col2.plotly_chart(fig, use_container_width=True)

    if st_side_filter=="전체":
        line_2019 = month_data[month_data["거래년도"] == 2019]
        line_2020 = month_data[month_data["거래년도"] == 2020]
        line_2021 = month_data[month_data["거래년도"] == 2021]
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(x=line_2019["거래월"], y=line_2019["판매금액"], mode='lines+markers+text', name='',
                                      hovertemplate="거래년도=2019년<br>판매금액(단위:백만 원)=%{y}", text=line_2019["판매금액"].apply(lambda x:"{:,}".format(int(x)))))
        fig_line.add_trace(go.Scatter(x=line_2020["거래월"], y=line_2020["판매금액"], mode='lines+markers+text', name='',
                                      hovertemplate="거래년도=2020년<br>판매금액(단위:백만 원)=%{y}", text=line_2020["판매금액"].apply(lambda x:"{:,}".format(int(x)))))
        fig_line.add_trace(go.Scatter(x=line_2021["거래월"], y=line_2021["판매금액"], mode='lines+markers+text', name='',
                                      hovertemplate="거래년도=2021년<br>판매금액(단위:백만 원)=%{y}", text=line_2021["판매금액"].apply(lambda x:"{:,}".format(int(x)))))
        fig_line.update_layout(autosize=True, plot_bgcolor="white", yaxis=dict(tickformat=","), hovermode="x unified")
    else:
        line_df = month_data
        fig_line = go.Figure()
        colors=['#3369C8','#EE5440','#00CC96']
        if st_side_filter==2021:
            linecolor=colors[0]
        elif st_side_filter==2020:
            linecolor = colors[1]
        else:
            linecolor = colors[2]
        fig_line.add_trace(go.Scatter(x=line_df["거래월"], y=line_df["판매금액"], mode='lines+markers+text', name="",hovertemplate="거래월=%{x}<br>판매금액(단위:백만 원)=%{y}", text=line_df["판매금액"].apply(lambda x:"{:,}".format(int(x))),line=dict(color=linecolor)))
        fig_line.update_layout(autosize=True, plot_bgcolor="white", yaxis=dict(tickformat=","))
    fig_line.update_traces(textposition='top center')
    fig_line.update_xaxes(showgrid=False)
    fig_line.update_yaxes(showgrid=True, gridcolor='LightPink', gridwidth=1)
    fig_line.update_layout(xaxis_title="월", yaxis_title="판매금액(단위:백만 원)")
    if st_side_filter=="전체":
        col3.subheader("전체 월별 판매 추이(단위:백만 원)")
    else:
        col3.subheader(str(st_side_filter)+"년 월별 판매 추이(단위:백만 원)")
    col3.plotly_chart(fig_line, use_container_width=True)

    ####################################################
    product_data_qty["판매금액"]=round(product_data_qty["판매금액"]/1000000)

    if st_side_filter=="전체":
        col4.subheader("전체 수량별 판매금액(단위:백만 원)")
        fig_scat = go.Figure()
        scat_2019 = product_data_qty[product_data_qty["거래년도"] == 2019]
        scat_2020 = product_data_qty[product_data_qty["거래년도"] == 2020]
        scat_2021 = product_data_qty[product_data_qty["거래년도"] == 2021]
        fig_scat.add_trace(go.Scatter(x=scat_2019["수량"], y=scat_2019["판매금액"], mode='markers',name='2019',text=scat_2019["품목분류"], hovertemplate="거래년도=2019년<br><b>품목분류=%{text}</b><br>수량=%{x}<br>판매금액(단위:백만 원)=%{y}"))
        fig_scat.add_trace(go.Scatter(x=scat_2020["수량"], y=scat_2020["판매금액"], mode='markers',name='2020',text=scat_2020["품목분류"], hovertemplate="거래년도=2020년<br><b>품목분류=%{text}</b><br>수량=%{x}<br>판매금액(단위:백만 원)=%{y}"))
        fig_scat.add_trace(go.Scatter(x=scat_2021["수량"], y=scat_2021["판매금액"], mode='markers',name='2021',text=scat_2021["품목분류"], hovertemplate="거래년도=2021년<br><b>품목분류=%{text}</b><br>수량=%{x}<br>판매금액(단위:백만 원)=%{y}"))

    else:
        col4.subheader(str(st_side_filter)+"년 수량별 판매금액(단위:백만 원)")
        scat=product_data_qty
        fig_scat = go.Figure()
        fig_scat.add_trace(
        go.Scatter(x=scat["수량"], y=scat["판매금액"], mode='markers', name=st_side_filter,
                       text=scat["품목분류"],marker=dict(color=linecolor), hovertemplate="<b>품목분류=%{text}</b><br>수량=%{x}<br>판매금액(단위:백만 원)=%{y}"
                   )
        )
    fig_scat.update_layout(xaxis_title="수량", yaxis_title="판매금액(단위:백만 원)")
    fig_scat.update_layout(autosize=True, plot_bgcolor="white", xaxis=dict(tickformat=",",zeroline=False),yaxis=dict(tickformat=",",zeroline=False))
    fig_scat.update_xaxes(showgrid=True, gridcolor='LightPink', gridwidth=1, showspikes=True)
    fig_scat.update_yaxes(showgrid=True, gridcolor='LightPink', gridwidth=1, showspikes=True)

    col4.plotly_chart(fig_scat,use_container_width=True)