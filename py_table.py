import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def app():
    ###################################data LOADING############################
    data = pd.read_csv('data/calender_data.csv', thousands=',')
    month_data = pd.read_csv('data/month_data.csv', thousands=',')
    discount_data = pd.read_csv('data/discount.csv', thousands=',')
    product_data = pd.read_csv('data/품목분류_data.csv', thousands=',')
    product_data_qty = pd.read_csv('data/품목분류_data_수량.csv', thousands=',')
    ###########################################################################
    ###############
    ###########################################################################
    st.title('판매 분석 대시보드')
    col_filter1, col_filter2, col_filter3, col_filter4 = st.beta_columns(4)
    del col_filter2, col_filter3, col_filter4
    st_side_filter = col_filter1.selectbox("년도를 선택하세요", ("전체", 2021, 2020, 2019))
    if st_side_filter == "전체":
        fig = go.Figure()
        # 총판매금액
        kpi_sum = round(data["판매금액"].sum() / 1000)
        fig.add_trace(go.Indicator(
            number={'valueformat': ',', 'font': {'size': 30}},
            mode="number",
            value=kpi_sum,
            domain={'row': 0, 'column': 0},
            title={'text': '<b>' + "총 판매금액(단위:천 원)" + '</b>', 'font': {'size': 17}}))

        # 작년대비증감률
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
            title={'text': '<b>' + "2021년 기준 작년 대비 증감률" + '</b>', 'font': {'size': 17}}))
        # 전체 수익 금액
        discount_sum = round(discount_data["수익금액"].sum() / 1000)
        fig.add_trace(go.Indicator(
            number={'valueformat': ',', 'font': {'size': 30}},
            mode="number",
            value=discount_sum,
            domain={'row': 0, 'column': 2},
            title={'text': '<b>' + "전체 수익 금액(단위:천 원)" + '</b>', 'font': {'size': 17}}))
        # 전체 할인율
        discount_rate = round(discount_data["할인율"].sum() / 3, 4)
        fig.add_trace(go.Indicator(
            number={'valueformat': '.2%', 'font': {'size': 30}},
            mode="number",
            value=discount_rate,
            domain={'row': 0, 'column': 3},
            title={'text': '<b>' + "전체 할인율(%)" + '</b>', 'font': {'size': 17}}))
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
        data_dec = data[data["거래년도"] == st_side_filter - 1]
        data = data[data["거래년도"] == st_side_filter]
        month_data = month_data[month_data["거래년도"] == st_side_filter]
        product_data = product_data[product_data["거래년도"] == st_side_filter]
        product_data_qty = product_data_qty[product_data_qty["거래년도"] == st_side_filter]
        fig = go.Figure()
        # 총판매금액
        kpi_sum = round(data["판매금액"].sum() / 1000)
        fig.add_trace(go.Indicator(
            number={'valueformat': ',', 'font': {'size': 30}},
            mode="number",
            value=kpi_sum,
            domain={'row': 0, 'column': 0},
            title={'text': '<b>' + str(st_side_filter) + "년 총 판매금액(단위: 천원)" + '</b>', 'font': {'size': 17}}))
        # 작년대비증감률
        if st_side_filter == 2019:
            fig.add_trace(go.Indicator(
                number={'valueformat': '.1%', 'font': {'size': 30}},
                mode="number",
                value=0,
                domain={'row': 0, 'column': 1},
                title={'text': '<b>' + str(st_side_filter) + "년 기준 작년 대비 증감률" + '</b>', 'font': {'size': 17}}))
        else:
            x_incdec = (data["판매금액"].sum() / data_dec["판매금액"].sum()) - 1
            x_incdec = round((x_incdec) * 100, 1)
            fig.add_trace(go.Indicator(
                number={'valueformat': '.1%', 'font': {'size': 30}},
                mode="number",
                value=x_incdec / 100,
                domain={'row': 0, 'column': 1},
                title={'text': '<b>' + str(st_side_filter) + "년 기준 작년 대비 증감률" + '</b>', 'font': {'size': 17}}))
        # 전체 할인 금액
        discount_sum = round(discount_data["수익금액"].sum() / 1000)
        fig.add_trace(go.Indicator(
            number={'valueformat': ',', 'font': {'size': 30}},
            mode="number",
            value=discount_sum,
            domain={'row': 0, 'column': 2},
            title={'text': '<b>' + str(st_side_filter) + "년 수익 금액(단위:천 원)" + '</b>', 'font': {'size': 17}}))
        # 전체 할인율
        discount_rate = round(discount_data["할인율"].sum(), 4)
        fig.add_trace(go.Indicator(
            number={'valueformat': '.2%', 'font': {'size': 30}},
            mode="number",
            value=discount_rate,
            domain={'row': 0, 'column': 3},
            title={'text': '<b>' + str(st_side_filter) + "년 할인율(%)" + '</b>', 'font': {'size': 17}}))
        fig.update_layout(
            grid={'rows': 1, 'columns': 4, 'pattern': "independent"},
            autosize=True,
            font={'color': "darkblue", 'family': "Balto"},
            height=100
        )
        st.plotly_chart(fig, use_container_width=True)
    table_chart=pd.read_csv('data/table.csv', thousands=',')
    if st_side_filter!="전체":
        table_chart=table_chart[table_chart["거래년도"]==st_side_filter]
    table_chart["판매금액"] = table_chart["판매금액"].apply(lambda x: "{:,}".format(x))
    table_chart["수익금액"] = table_chart["수익금액"].apply(lambda x: "{:,}".format(x))
    #table_chart["수량"] = table_chart["수량"].apply(lambda x: "{:,}".format(int(x)))
    #table_chart["할인율"] = table_chart["할인율"].apply(lambda x: "{:,}".format(float(x)))
    table_chart=table_chart.head(100)
    #table_chart=table_chart.drop(['거래년도'],axis=1)
    tmp=list(table_chart.columns)
    del tmp[-1]
    del tmp[-1]
    del tmp[-1]
    del tmp[-1]
    table_chart=table_chart.style.set_properties(subset=tmp, **{'text-align': 'left'}).set_table_styles([dict(selector='th', props=[('text-align', 'left')])])

    col1,col2 = st.beta_columns(2)
    #table_chart.set_index('column', inplace=True)
    col1.dataframe(table_chart,height=600,width=2000)
    col2.markdown("<h5 style='text-align: center; margin:0 0;'>Demo에 사용한 데이터는 kaggle의 E-commerce 사용<br>(E-commerce의 Order Date Column 에서 year에 +4~+6를 랜덤으로 더해줌)</h5>",
                unsafe_allow_html=True)

    raw_data=pd.read_csv('data/ecommerce.csv',dtype={"Sales":"string","Quantity":"string","Profit":"string"})
    col2.subheader("")
    if col2.checkbox("원본 데이터 보기"):
        col2.dataframe(raw_data.head(100),height=494,width=1000)
    #st.plotly_chart(fig, use_container_width=True)
    #st.table(table_chart)