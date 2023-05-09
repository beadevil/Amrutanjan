from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from io import BytesIO
import requests
import os
from PIL import Image
import matplotlib.pyplot as plt



response = requests.get('https://www.amrutanjan.com/images/logo-new.png')
image = Image.open(BytesIO(response.content))


st.sidebar.image(image, caption='AMRUTANJAN')

st.sidebar.success("# `This Web App built in Python and Streamlit by  MAYUKH BHAUMIK 👨🏼‍💻`")


with st.sidebar:
        selected = option_menu("Menu", ["Home", 'Super Stockist',"Stockist","SUB Stockist","Stockist & SUB Stockist"], 
        icons=['house', ], default_index=0)


if selected == "Home" :
    

    col1, col2, col3= st.columns(3)

    with col1:
        st.title("AMRUTANJAN HEALTHCARE")
    with col2:
        st.write()

    with col3:
        st.image(image, caption='AMRUTANJAN')

    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")


    df_1 = pd.read_excel("town_Super_Stockist.xlsx",sheet_name="Super Stockist")
    df_miss_1 = pd.read_excel("town_Super_Stockist.xlsx",sheet_name="Missing Super Stockist")
    df_2 = pd.read_excel("town_Stockist.xlsx",sheet_name="Stockist")
    df_miss_2 = pd.read_excel("town_Stockist.xlsx",sheet_name="Missing Stockist")
    df_3 = pd.read_excel("town_SUB_Stockist.xlsx",sheet_name="SUB Stockist")
    df_miss_3 = pd.read_excel("town_SUB_Stockist.xlsx",sheet_name="Missing SUB Stockist")

    df = df_1.append(df_2, ignore_index=True)
    df = df.append(df_3, ignore_index=True)
    df_miss = df_miss_1.append(df_miss_2, ignore_index=True)
    df_miss = df_miss.append(df_miss_3, ignore_index=True)

    df_state = df.append(df_miss, ignore_index=True)



if selected == "Super Stockist":
    df = pd.read_excel("town_Super_Stockist.xlsx",sheet_name="Super Stockist")
    df_miss = pd.read_excel("town_Super_Stockist.xlsx",sheet_name="Missing Super Stockist")
    df_state = df.append(df_miss, ignore_index=True)

if selected == "Stockist":
    df = pd.read_excel("town_Stockist.xlsx",sheet_name="Stockist")
    df_miss = pd.read_excel("town_Stockist.xlsx",sheet_name="Missing Stockist")
    df_state = df.append(df_miss, ignore_index=True)

if selected == "SUB Stockist":
    df = pd.read_excel("town_SUB_Stockist.xlsx",sheet_name="SUB Stockist")
    df_miss = pd.read_excel("town_SUB_Stockist.xlsx",sheet_name="Missing SUB Stockist")
    df_state = df.append(df_miss, ignore_index=True)

if selected == "Stockist & SUB Stockist":
    df_s = pd.read_excel("town_Stockist.xlsx",sheet_name="Stockist")
    df_miss_s = pd.read_excel("town_Stockist.xlsx",sheet_name="Missing Stockist")

    df_ss = pd.read_excel("town_SUB_Stockist.xlsx",sheet_name="SUB Stockist")
    df_miss_ss = pd.read_excel("town_SUB_Stockist.xlsx",sheet_name="Missing SUB Stockist")

    df = df_s.append(df_ss, ignore_index=True)
    df_miss = df_miss_s.append(df_miss_ss, ignore_index=True)

    df_state_s = df_s.append(df_miss_s, ignore_index=True)
    df_state_ss = df_ss.append(df_miss_ss, ignore_index=True)

    df_state = df_state_s.append(df_state_ss, ignore_index=True)


if selected == "Home" or selected == "Super Stockist" or selected == "Stockist" or selected == "SUB Stockist" or selected == "Stockist & SUB Stockist" :

    state = list(df_state["State"].unique())

    state.insert(0, "SELECT")

    sb_state=st.sidebar.selectbox('SELECT STATE :',state)

    if sb_state=="SELECT":
        dff_wow=df[df["State"].isin(df_state["State"].unique())]
    else:
        dff_wow=df[df["State"].isin([sb_state])]
    
    town = list(dff_wow["Address"].unique())

    town.insert(0, "SELECT")

    sb_adrs = st.sidebar.selectbox('SELECT TOWN',town)


    dff_a=dff_wow[dff_wow["Address"].isin([sb_adrs])]
    dff_a['Listed']=1





    dff_add_s=dff_wow[~dff_wow["Address"].isin([sb_adrs])]
#    dff_add_s["Listed"]=1


    dff_add_m=dff_add_s[dff_add_s["Type"].isin(["Super Stockist"])]

    dff_add_m1=dff_add_s[dff_add_s["Type"].isin(["Stockist"])]

    dff_add_m2=dff_add_s[dff_add_s["Type"].isin(["SUB Stockist"])]

    if selected == "Home" :
        dff_add_m["Listed"]=0.2
        dff_add_m1["Listed"]=0.15
        dff_add_m2["Listed"]=0.1

    elif selected == "Stockist & SUB Stockist":
        dff_add_m1["Listed"]=0.15
        dff_add_m2["Listed"]=0.1
    else :
        dff_add_m["Listed"]=0.1
        dff_add_m1["Listed"]=0.1
        dff_add_m2["Listed"]=0.1
        

    dff = dff_a.append(dff_add_m, ignore_index=True)
    dff = dff.append(dff_add_m1, ignore_index=True)
    dff = dff.append(dff_add_m2, ignore_index=True)

    chennai ={ 'State': ["Tamilnadu"],'Address':["Chennai, Chennai District, Tamil Nadu, 600001, India"],'Lat':[13.0836939],'Long':[80.270186],'Type':["HEAD OFFICE"],"Listed":[1]}
    df_chennai = pd.DataFrame(chennai)
    dff= dff.append(df_chennai)



    dff.dropna(
        axis=0,
        how='any',
#       thresh=None,
        subset=None,
        inplace=True
    )

    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")

    st.sidebar.write("## Ploted Town No. :",len(dff))
    st.sidebar.write("## Missing Town No. :",len(df_miss))

    if selected == "Home" :

        if sb_state=="SELECT" :

            color_scale = [(0, 'blue'),(.05, 'green'),(.1, 'purple'), (1, 'red')]

            fig = px.scatter_mapbox(dff, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name="Address", 
#                        color='rgb(242, 177, 172)',
                        hover_data=["Type"],
                        color="Listed",
                        color_continuous_scale=color_scale,
                        size="Listed",
                        zoom=4, 
#                        height=1800,
#                        width=1800
                        )

        else:
            color_scale = [(0, 'blue'),(.05, 'green'),(.1, 'purple'), (1, 'red')]

            fig = px.scatter_mapbox(dff, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name="Address", 
#                        color='rgb(242, 177, 172)',
                        hover_data=["Type"],
                        color="Listed",
                        color_continuous_scale=color_scale,
                        size="Listed",
                        zoom=6.3, 
#                        height=1800,
#                        width=1800
                        )
            

        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#       fig.show()
        fig.update_layout(width=800, height=700,)
        st.plotly_chart(fig,width=800, height=700,)

    

    else :
        if sb_state=="SELECT" :
            
            if selected=="Super Stockist":
                color_scale = [(0, 'purple'), (1,'red')]
            elif selected=="Stockist":
                color_scale = [(0, 'green'), (1,'red')]
            elif selected=="SUB Stockist":
                color_scale = [(0, 'blue'), (1,'red')]
            elif selected=="Stockist & SUB Stockist":
                color_scale = [(0, 'blue'), (.05, 'green'), (1,'red')]

            fig = px.scatter_mapbox(dff, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name="Address", 
#                        color='rgb(242, 177, 172)',
                        hover_data=["Type"],
                        color="Listed",
                        color_continuous_scale=color_scale,
                        size="Listed",
                        zoom=4.5, 
#                        height=1800,
#                        width=1800
                        )
        
        else:
            if selected=="Super Stockist":
                color_scale = [(0, 'purple'), (1,'red')]
            elif selected=="Stockist":
                color_scale = [(0, 'green'), (1,'red')]
            elif selected=="SUB Stockist":
                color_scale = [(0, 'blue'), (1,'red')]
            elif selected=="Stockist & SUB Stockist":
                color_scale = [(0, 'blue'), (.05, 'green'), (1,'red')]

            fig = px.scatter_mapbox(dff, 
                        lat="Lat", 
                        lon="Long", 
                        hover_name="Address", 
#                        color='rgb(242, 177, 172)',
                        hover_data=["Type"],
                        color="Listed",
                        color_continuous_scale=color_scale,
                        size="Listed",
                        zoom=6.3, 
#                        height=1800,
#                        width=1800
                        )
        
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#       fig.show()
        fig.update_layout(width=900, height=900,)
        st.plotly_chart(fig,width=900, height=900,)


    if sb_adrs!="SELECT":
        st.sidebar.write("")
        st.sidebar.write("")
        st.sidebar.markdown("# Address :")
        for i in dff_a["Address"] :
            st.sidebar.write(i)
        st.sidebar.markdown("# Type :")
        for i in dff_a["Type"] :
            st.sidebar.write(i)
        st.sidebar.markdown("# Outlet Lat :")
        for i in dff_a["Lat"] :
            st.sidebar.write(i)
        st.sidebar.markdown("# Outlet Long :")
        for i in dff_a["Long"] :
            st.sidebar.write(i)

    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("")
    
    if sb_state!="SELECT" :

        if selected == "Home" or selected == "Super Stockist" or selected == "Stockist" or selected == "SUB Stockist" :
            dff_miss=df_miss[df_miss["State"].isin([sb_state])]
            st.sidebar.markdown("# Missing Town Names :")
            c=1
            for i in dff_miss["Town"] :
                st.sidebar.write(c,". ",i.split(",")[0])
                c=c+1

        elif selected == "Stockist & SUB Stockist" :
            dff_miss_p=df_miss[df_miss["State"].isin([sb_state])]

            dff_miss_s=dff_miss_p[dff_miss_p["Type"].isin(["Stockist"])]
            st.sidebar.markdown("# Missing Stockist's Town Names :")
            c=1
            for i in dff_miss_s["Town"] :
                st.sidebar.write(c,". ",i.split(",")[0])
                c=c+1

            dff_miss_ss=dff_miss_p[dff_miss_p["Type"].isin(["SUB Stockist"])]
            st.sidebar.markdown("# Missing SUB Stockist's Town Names :")
            c=1
            for i in dff_miss_ss["Town"] :
                st.sidebar.write(c,". ",i.split(",")[0])
                c=c+1

    else:
        if selected == "Home" :

            dff_miss_s=df_miss[df_miss["Type"].isin(["Super Stockist"])]
            st.sidebar.markdown("# Missing Super Stockist's Town Names :")
            c=1
            for i in dff_miss_s["Town"] :
                st.sidebar.write(c,". ",i.split(",")[0])
                c=c+1

            dff_miss_ss=df_miss[df_miss["Type"].isin(["Stockist"])]
            st.sidebar.markdown("# Missing Stockist's Town Names :")
            c=1
            for i in dff_miss_ss["Town"] :
                st.sidebar.write(c,". ",i.split(",")[0])
                c=c+1

            dff_miss_s=df_miss[df_miss["Type"].isin(["SUB Stockist"])]
            st.sidebar.markdown("# Missing SUB Stockist's Town Names :")
            c=1
            for i in dff_miss_s["Town"] :
                st.sidebar.write(c,". ",i.split(",")[0])
                c=c+1


        elif selected == "Super Stockist" or selected == "Stockist" or selected == "SUB Stockist" :
            df_miss_state=df_miss[df_miss["State"].isin([sb_state])]
            st.sidebar.markdown("# Missing "+selected+"'s Town Names :")
            c=1
            for i in df_miss["Town"] :
                st.sidebar.write(c,". ",i.split(",")[0])
                c=c+1

        elif selected == "Stockist & SUB Stockist" :

            dff_miss_s=df_miss[df_miss["Type"].isin(["Stockist"])]
            st.sidebar.markdown("# Missing Stockist's Town Names :")
            c=1
            for i in dff_miss_s["Town"] :
                st.sidebar.write(c,". ",i.split(",")[0])
                c=c+1

            dff_miss_ss=df_miss[df_miss["Type"].isin(["SUB Stockist"])]
            st.sidebar.markdown("# Missing SUB Stockist's Town Names :")
            c=1
            for i in dff_miss_ss["Town"] :
                st.sidebar.write(c,". ",i.split(",")[0])
                c=c+1

    
     