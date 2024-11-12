# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import datetime
from PIL import Image, ImageDraw, ImageFont
import plotly.graph_objects as go
import random
import json
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


def local_pvModel(file_name):
    st.markdown(
            f'<iframe src=' + file_name + ' height = "860" width = "100%"></iframe>',
            unsafe_allow_html=True,
    )


def generate_stockpile_data(dates):
    # 设置固定的种子，以确保每次运行结果相同
    random.seed(42)

    # 生成Stockpile名称
    stockpile_names = ["S1", "S2", "S3", "S4", "S5", "S6"]

    # 定义每种矿物性质的合理范围
    hardness_range = (40, 60)
    fe_range = (30, 70)
    silica_range = (5, 25)
    f80_range = (0, 100)
    f50_range = (0, 100)
    clay_range = (5, 30)
    phos_range = (0.1, 1.5)

    # 初始化数据列表
    stockpile_data = []

    # 生成每个Stockpile的数据
    for name in stockpile_names:
        data = {
            "Stockpile": name,
            "Date": [],
            "Hardness": [],
            "Fe%": [],
            "Silica%": [],
            "F80": [],
            "F50": [],
            "Clay%": [],
            "Phos%": []
        }
        for date in dates:
            data["Date"].append(date.date())
            data["Hardness"].append(random.uniform(*hardness_range))
            data["Fe%"].append(random.uniform(*fe_range))
            data["Silica%"].append(random.uniform(*silica_range))
            data["F80"].append(random.uniform(*f80_range))
            data["F50"].append(random.uniform(*f50_range))
            data["Clay%"].append(random.uniform(*clay_range))
            data["Phos%"].append(random.uniform(*phos_range))
        stockpile_data.append(data)

    # 将数据转换为DataFrame
    stockpile_dfs = [pd.DataFrame(data) for data in stockpile_data]

    return stockpile_dfs


# Function to annotate the image
def annotate_image(image_path, t1, t2, t3):
    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Define font and color
    try:
        font = ImageFont.truetype("arial.ttf", 40)  # Ensure the font is accessible or use default
    except IOError:
        font = ImageFont.load_default()

    color = (255, 0, 0)  # Red color for the text

    # Draw text on the image at specified positions
    draw.text((270, 20), f"t1={t1}s", fill=color, font=font)  # Replace with exact coordinates for t1
    draw.text((50, 130), f"t2={t2}s", fill=color, font=font)  # Replace with exact coordinates for t3
    draw.text((70, 280), f"t3={t3}s", fill=color, font=font)  # Replace with exact coordinates for t5
    return image


def main():
    st.set_page_config(page_title='Citic Smart Tray App', initial_sidebar_state='expanded')
    st.logo("citic_logo.png", size="large")

    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # 初始化认证相关的state
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None

    name, authentication_status, username = authenticator.login(fields={'form_name': 'Sino Iron - Ore Tracking and Prediction App', 'location': 'main'})

    if authentication_status:
        # Sidebar

        st.sidebar.toggle("Dark Mode")
        st.sidebar.header(":rainbow[Smart Ore Tracking App]")
        st.sidebar.image("dumpTruck.png", width=240)
        st.sidebar.subheader("***Next Gen Mine-to-Mill Intelligence***", divider='gray')

        app_chosen = st.sidebar.radio(
                        "Please Select App Function:",
                        ["Ore Stockpile Filling Prediction",
                         "Mill Feed and Performance Forecast",
                         "Configure Process Parameters",
                         "Configure Database Connection",]
        )


        ################################################
        if app_chosen == "Ore Stockpile Filling Prediction":
            ### App 1 ##################
            st.subheader("RoM Ore Stockpile Reconcilliation", divider="rainbow")
            ##################################################
            refresh_interval = st.selectbox("Please Select Data Refresh Interval",
                                ["5 mins", "10 mins", "30 mins", "60 mins"],)
            cl0 = st.columns([1, 1, 1, 1], gap="medium", vertical_alignment="center")
            with cl0[0]:
                st.button("Confirm", use_container_width=True)
            with cl0[-1]:
                st.button("Refresh Now", use_container_width=True)

            categories = ["S1-1", "S1-2", "S1-3", "S2-1", "S2-2", "S2-3",
                          "S3-1", "S3-2", "S3-3", "S4-1", "S4-2", "S4-3",
                          "S5-1", "S5-2", "S5-3", "S6-1", "S6-2", "S6-3"]
            values = [68, 72, 56, 39, 19, 55, 67, 19, 53, 17, 72, 87, 66, 24, 55, 40, 89, 54]
            colors = [
                "#6AABF0", "#4B91E8", "#2F78D0", "#FFB685", "#F59A55", "#D47A30",
                "#89E0B5", "#68D69E", "#4CB47C", "#F7E08A", "#F4D35E", "#D1B342",
                "#7ADFF2", "#55D0E8", "#38A9BE", "#F2A5B3", "#EC7F9D", "#C86479"
            ]

            # 定义每个柱的hover信息
            hover_text = [
                "orebody A: 29%<br>orebody B: 27%<br>orebody C: 28%<br>orebody D: 23%",  # S1-1
                "orebody A: 29%<br>orebody B: 27%<br>orebody C: 28%<br>orebody D: 23%",  # S1-2
                "orebody A: 30%<br>orebody B: 28%<br>orebody C: 26%<br>orebody D: 22%",  # S1-3
                "orebody A: 25%<br>orebody B: 24%<br>orebody C: 26%<br>orebody D: 25%",  # S2-1
                "orebody A: 26%<br>orebody B: 23%<br>orebody C: 27%<br>orebody D: 24%",  # S2-2
                "orebody A: 27%<br>orebody B: 25%<br>orebody C: 28%<br>orebody D: 20%",  # S2-3
                "orebody A: 29%<br>orebody B: 25%<br>orebody C: 27%<br>orebody D: 19%",  # S3-1
                "orebody A: 30%<br>orebody B: 27%<br>orebody C: 25%<br>orebody D: 18%",  # S3-2
                "orebody A: 28%<br>orebody B: 26%<br>orebody C: 24%<br>orebody D: 22%",  # S3-3
                "orebody A: 26%<br>orebody B: 24%<br>orebody C: 27%<br>orebody D: 23%",  # S4-1
                "orebody A: 25%<br>orebody B: 23%<br>orebody C: 28%<br>orebody D: 24%",  # S4-2
                "orebody A: 27%<br>orebody B: 25%<br>orebody C: 26%<br>orebody D: 22%",  # S4-3
                "orebody A: 26%<br>orebody B: 25%<br>orebody C: 24%<br>orebody D: 25%",  # S5-1
                "orebody A: 30%<br>orebody B: 28%<br>orebody C: 22%<br>orebody D: 20%",  # S5-2
                "orebody A: 29%<br>orebody B: 27%<br>orebody C: 23%<br>orebody D: 21%",  # S5-3
                "orebody A: 32%<br>orebody B: 30%<br>orebody C: 23%<br>orebody D: 15%",  # S6-1
                "orebody A: 33%<br>orebody B: 31%<br>orebody C: 22%<br>orebody D: 14%",  # S6-2
                "orebody A: 31%<br>orebody B: 28%<br>orebody C: 24%<br>orebody D: 17%",  # S6-3
            ]

            # 创建柱状图
            fig = go.Figure(data=[
                go.Bar(
                    x=categories,
                    y=values,
                    marker_color=colors,
                    text=values,
                    textposition='outside',
                    hovertext=hover_text,
                    hoverinfo="text"
                )
            ])

            # 更新布局
            fig.update_layout(
                title=f"Last updated: {datetime.datetime.now().strftime('%I:%M:%S %p %d-%m-%Y')}",
                xaxis_title="Stockpile",
                yaxis_title="Stockpile Filling Level (%)",
                yaxis=dict(range=[0, 100]),
                showlegend=False,
                bargap=0.05
            )
            st.plotly_chart(fig, use_container_width=True)

        elif app_chosen == "Mill Feed and Performance Forecast":
            ### App 2 ##################
            st.subheader("Mill Feed Prediction", divider="rainbow")
            ##################################################
            refresh_interval_millfeed = st.selectbox("Please Select Data Refresh Interval",
                                ["5 mins", "10 mins", "30 mins", "60 mins"],)
            cl1 = st.columns([1, 1, 1, 1], gap="medium", vertical_alignment="center")
            with cl1[0]:
                st.button("Confirm", key="confirm_mill_feed", use_container_width=True)
            with cl1[-1]:
                st.button("Refresh Now", key="refresh_mill_feed", use_container_width=True)
            # 示例数据
            dates_mill = pd.date_range(start="2024-10-06", end="2024-12-29", freq="7D")  # 每周的数据
            mill_names = ["Mill #1", "Mill #2", "Mill #3", "Mill #4", "Mill #5", "Mill #6"]
            throughput_data = [
                [1600, 1450, 1550, 1300, 1600, 1250, 1450, 1500, 1600, 1250, 1550, 1450],
                [1200, 1300, 1150, 1350, 1200, 1100, 1250, 1400, 1200, 1300, 1250, 1450],
                [1000, 1150, 1020, 900, 1050, 980, 1100, 1150, 1250, 1050, 1200, 1000],
                [1400, 1450, 1300, 1250, 1400, 1150, 1350, 1450, 1500, 1300, 1550, 1600],
                [1100, 1050, 1150, 1250, 1100, 1200, 1150, 1300, 1250, 1350, 1200, 1400],
                [800, 950, 870, 800, 850, 900, 950, 800, 860, 910, 800, 850]
            ]

            # 创建图表
            fig = go.Figure()

            # 添加每条曲线
            for mill_name, data in zip(mill_names, throughput_data):
                fig.add_trace(go.Scatter(
                    x=dates_mill,
                    y=data,
                    mode='lines',
                    name=mill_name,
                    line=dict(shape='spline')  # 设置线条为平滑曲线
                ))

            # 更新布局
            fig.update_layout(
                title=f"Last updated: {datetime.datetime.now().strftime('%I:%M:%S %p %d-%m-%Y')}",
                xaxis_title="Date and Time",
                yaxis_title="Throughput Rate - tph",
            )
            st.plotly_chart(fig, use_container_width=True)

            stockpile_dfs = generate_stockpile_data(dates_mill)

            selected_stockpiles = st.multiselect('Select Stockpiles to plot', ["S1", "S2", "S3", "S4", "S5", "S6"],
                                                 default=["S1", "S2", "S3"])

            # 用户选择要绘制的数据类型
            data_types = ["***Hardness***", "***Fe%***", "***Silica%***", "***F80***", "***F50***", "***Clay%***", "***Phos%***"]
            selected_data_type = st.radio("Select Data Type", data_types, index=0, horizontal=True, label_visibility="collapsed").replace("***", "")
            # 绘制图表
            fig_mill1 = go.Figure()

            for stockpile in selected_stockpiles:
                stockpile_df = next(df for df in stockpile_dfs if df["Stockpile"].iloc[0] == stockpile)

                fig_mill1.add_trace(go.Scatter(x=stockpile_df["Date"], y=stockpile_df[selected_data_type], mode='lines',
                                         name=f'Feed Belt - {stockpile}', line=dict(shape='spline')))

            fig_mill1.update_layout(
                title=f"Last updated: {datetime.datetime.now().strftime('%I:%M:%S %p %d-%m-%Y')}",
                xaxis_title="Date",
                yaxis_title=f"{selected_data_type}",
                legend_title="Stockpile and Data Type",
                template="plotly_dark"
            )
            st.plotly_chart(fig_mill1, use_container_width=True)




            selected_mill = st.multiselect('Please Select AG Mill For Throughput Prediction', mill_names,
                                                 default=["Mill #1", "Mill #2", "Mill #3"])
            st.button("Confirm", key="confirm_mill_prediction")
            # 读取桌面上的XLSX文件
            file_path = './resources/Generated_Mill_Data-test.xlsx'
            mill_prediction_data = pd.read_excel(file_path)

            # Prepare the plotly figures
            fig_mill_predict = go.Figure()

            # Iterate through selected mills and add traces for each
            for mill in selected_mill:
                real_column = f'{mill}_Real-Data'
                xgb_column = f'{mill}_XGB'

                # Add Real-Data trace
                fig_mill_predict.add_trace(go.Scatter(x=mill_prediction_data['Time'],
                                         y=mill_prediction_data[real_column],
                                         mode='lines',
                                         name=f'{mill} Real-Data'))

                # Add XGB trace
                fig_mill_predict.add_trace(go.Scatter(x=mill_prediction_data['Time'],
                                         y=mill_prediction_data[xgb_column],
                                         mode='lines',
                                         name=f'{mill} XGB Prediction'))

            # Customize the layout
            fig_mill_predict.update_layout(
                title=f"Last updated: {datetime.datetime.now().strftime('%I:%M:%S %p %d-%m-%Y')} <br>Throughput Predictions for Selected Mills ",
                xaxis_title="Time",
                yaxis_title="Throughput",
                legend_title="Mill and Data Type",
                template="plotly_dark"
            )

            # Show the plot in Streamlit
            st.plotly_chart(fig_mill_predict, use_container_width=True)

        elif app_chosen == "Configure Process Parameters":
            ### App 3 ##################
            st.subheader("Configure Process Parameters", divider="rainbow")
            st.markdown("**Current Ore Processing Flowsheet**")
            ##################################################
            image_path = "./resources/processing flowsheet.png"
            image = Image.open(image_path)

            # Initialize original values in session state if not already present
            if "original_values" not in st.session_state:
                st.session_state.original_values = {
                    "t1": 2.0, "t2": 3.0, "t3": 4.0, "t4": 5.0,
                    "t5": 6.0, "t6": 5.0, "t7": 4.0, "t8": 3.0,
                    "t9": 2.0, "t10": 12.0
                }

            if "annotated_image" not in st.session_state:
                st.image(image, use_column_width=True)
            else:
                # Display the (possibly updated) image
                st.image(st.session_state.annotated_image, use_column_width=True)

            st.markdown("**Please set the ore transport delay time -s**")

            cl2 = st.columns([1, 1], gap="medium", )
            with cl2[0]:
                t1 = st.number_input("*Dump Truck → Feed Chute*", value=st.session_state.original_values["t1"], step=1.0)
                t3 = st.number_input("*Gyratory Crusher → Bottom Bin*", value=st.session_state.original_values["t3"], step=1.0)
                t5 = st.number_input("*Belt Feeder → Long Belt*", value=st.session_state.original_values["t5"], step=1.0)
                t7 = st.number_input("*Stacker → RoM Ore Stockpile*", value=st.session_state.original_values["t7"], step=1.0)
                t9 = st.number_input("*Feeder → Mill Feed Belt*", value=st.session_state.original_values["t9"], step=1.0)
            with cl2[1]:
                t2 = st.number_input("*Gyratory Crusher*", value=st.session_state.original_values["t2"], step=1.0)
                t4 = st.number_input("*Bottom Bin → Belt Feeder*", value=st.session_state.original_values["t4"], step=1.0)
                t6 = st.number_input("*Long Belt → Stacker*", value=st.session_state.original_values["t6"], step=1.0)
                t8 = st.number_input("*RoM Ore Stockpile → Feeder*", value=st.session_state.original_values["t8"], step=1.0)
                t10 = st.number_input("*Mill Feed Belt → AG Mill*", value=st.session_state.original_values["t10"], step=1.0)
            # st.button("Confirm Delay Time", key="set_button", use_container_width=True)

            # Confirm button to apply the delay time and update the image
            if st.button("Confirm Delay Time", key="set_button", use_container_width=True):

                new_values = {"t1": t1, "t2": t2, "t3": t3, "t4": t4, "t5": t5, "t6": t6, "t7": t7, "t8": t8, "t9": t9,
                              "t10": t10}
                # Check if any value has changed
                if new_values != st.session_state.original_values:
                    st.session_state.original_values = new_values  # Update the stored values
                    st.session_state.annotated_image = annotate_image(image_path, t1, t2,
                                                                      t3)  # Update the session state image
                    st.rerun()  # Rerun the app

        else:  # "Configure Database Connection"
            ### App 4 ##################
            st.subheader("Configure Database Connection", divider="rainbow")
            st.markdown("**Please configure the API json call for the database**")
            ##################################################
            # Define initial JSON data
            initial_data = {
                "database": {
                    "type": "postgresql",
                    "host": "localhost",
                    "port": 5432,
                    "database_name": "my_database",
                    "username": "my_user",
                    "password": "my_password"
                }
            }

            # Dropdown for database type selection
            db_type = st.selectbox("Choose Database Type", ["postgresql", "mysql", "sqlite"], index=0)
            initial_data['database']['type'] = db_type  # Update JSON data with selected type

            # Convert to JSON string for editing
            json_str = json.dumps(initial_data, indent=4)
            json_input = st.text_area("Edit JSON Data", value=json_str, height=300)

            # Confirmation button
            if st.button("Confirm and Update JSON"):
                try:
                    updated_data = json.loads(json_input)
                    st.success("JSON data updated successfully!")
                    st.json(updated_data)
                except json.JSONDecodeError:
                    st.error("Invalid JSON format. Please check your input.")

        st.sidebar.markdown("###")
        st.sidebar.markdown(f"***Welcome {name}!***")
        authenticator.logout("Logout", 'sidebar')


    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')


    #############################################################################################################################################################################
    st.markdown(
        f"""
            <style>
                .reportview-container .main .block-container{{
                    max-width: 1500px;
                    padding-top: 1rem;
                    padding-right: 1rem;
                    padding-left: 1rem;
                    padding-bottom: 1rem;
                }}

            </style>
            """,
        unsafe_allow_html=True,
    )

    footer = """  
            <style>
                .footer {
                position: fixed;
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #50575b;
                color: white;
                text-align: center;
                }
            </style>

            <div class="footer">
                <p>Visit us @ https://citicpacificmining.com | © 2024 Copyright Citic Pacific Mining  </p>
            </div>
        """

    st.markdown(footer, unsafe_allow_html=True)

if __name__ == "__main__":
    main()



