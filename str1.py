import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
st.set_page_config(page_title="Cyber Crime Analysis",page_icon="🔒",layout="wide") 
st.markdown("""
<div style="
background:#1E3A8A;
padding:15px;
border-radius:10px;
text-align:center;
margin-bottom:20px;">
<h1 style="color:white; margin:0;">
🛡️ Cyber Attack Analytics & Trends
</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Main Background */
.stApp{
    background-color:#0B0B10;
}
/* Main Content */
.main .block-container{
    background-color:#0B0B10;
    padding-top:1rem;
}
/* Sidebar ko upar lao */
section[data-testid="stSidebar"] .block-container{
    padding-top:0.5rem !important;
}

/* Navigation aur Filters ke gaps kam */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2{
    margin-top:0 !important;
    margin-bottom:5px !important;
}

section[data-testid="stSidebar"] hr{
    margin:5px 0 !important;
}           
/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#111117;
    border-right:1px solid #2A2A2A;
}
/* Plotly Graph Background */
div[data-testid="stPlotlyChart"]{
    background-color:#15151C;
    border-radius:12px;
    padding:10px;
    border:1px solid #2E2E38;
}
/* Metric Cards */
[data-testid="stMetric"]{
    background-color:#15151C;
    border:1px solid #2E2E38;
    border-radius:10px;
    padding:10px;
}
/* Selectbox */
div[data-baseweb="select"] > div{
    background:#15151C;
    color:white;
    border:1px solid #333;
}
/* Radio */
.stRadio label{
    color:white;
}
h1,h2,h3,h4,p,label{
    color:white;
}
            div[data-testid="stPlotlyChart"]{
    background:#000000;
    border:1px solid #333333;
    border-radius:12px;
    padding:10px;
}
    div[data-testid="stPlotlyChart"]{
    background: transparent !important;
    border: none !important;
    padding: 0px !important;
    box-shadow: none !important;
}       
</style>
""", unsafe_allow_html=True)
df=pd.read_csv("Global_Cybersecurity_Threats_20-2.csv")
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "",
    [
        "ℹ️ About",
        "🧹 Data Cleaning",
        "🏠 Dashboard",
        "📊 Attack Analytics",
        "📈 Industry Analytics",
        "🌍 Hotspot Map",
        "💡 Insights"
    ]
)

st.sidebar.markdown("---")
st.sidebar.header("Filters")
country=st.sidebar.selectbox("Country",["All"]+sorted(df["Country"].unique().tolist()))
year=st.sidebar.selectbox("Year",["All"]+sorted(df["Year"].unique().tolist()))
industry=st.sidebar.selectbox("Target Industry",["All"]+sorted(df["Target Industry"].unique().tolist()))
attack_type=st.sidebar.selectbox("Attack_ID",["All"]+sorted(df["Attack_ID"].unique().tolist()))
attack_source=st.sidebar.selectbox("Attack Source",["All"]+sorted(df["Attack Source"].unique().tolist()))
filtered_df = df.copy() 
if country != "All":
    filtered_df = filtered_df[filtered_df["Country"] == country]
if year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == year]
if industry != "All":
    filtered_df = filtered_df[filtered_df["Target Industry"] == industry]
if attack_type != "All":
    filtered_df = filtered_df[filtered_df["Attack_ID"] == attack_type]
if attack_source != "All":
    filtered_df = filtered_df[filtered_df["Attack Source"] == attack_source]


if page == "🏠 Dashboard":
            loss = filtered_df["Financial Loss in Million  Doller"].sum()
            users = filtered_df["Number of Affected Users"].sum()
            max_hr = filtered_df["Incident Resolution Time (in Hours)"].max()
            attack_count = len(filtered_df)
            industry_count = filtered_df["Target Industry"].nunique()
            st.markdown("<br>",unsafe_allow_html=True)
            st.markdown("""
            <style>
            [data-testid="stMetric"]{
                background-color:#1E293B;
                border:1px solid #3B82F6;
                box-shadow:0 4px 10px rgba(0,0,0,0.3);
                padding:8px;
                border-radius:8px;
                min-height:90px;
            }
            </style>
            """, unsafe_allow_html=True)
            c1, c2, c3, c4, c5 = st.columns(5)
            with c1:
                st.metric("💰 Total Loss ($)", f"{loss:.2f}M")
            with c2:
                st.metric("👥 Total Affected Users", f"{users/1000000:.2f}M")
            with c3:
                st.metric("⏱️ Max Hr", max_hr)
            with c4:
                st.metric("🛡️ Total Attack Count", attack_count)
            with c5:
                st.metric("🏭 Industry Count", industry_count)
            country_loss = (
                filtered_df.groupby("Country")["Financial Loss in Million  Doller"]
                .sum()
                .reset_index()
                .sort_values(by="Financial Loss in Million  Doller", ascending=True)
            )
            fig1 = px.bar(
                country_loss,
                x="Financial Loss in Million  Doller",
                y="Country",
                orientation="h",
                title="Total Financial Loss by Country"
            )
            fig1.update_traces(
            marker=dict(
            color=[
            "#0085FF",
            "#1E90FF",
            "#3399FF",
            "#4DA6FF",
            "#66B2FF",
            "#80BFFF",
            "#99CCFF",
            "#B3D9FF",
            "#CCE6FF",
            "#A6D8FF"
        ]
        )
            )
            
            fig1.update_layout(
            paper_bgcolor="#0B0B10",
            plot_bgcolor="#0B0B10",
            font_color="white",
            title_font=dict(color="#F4B400", size=22),   # Golden heading
            height=350,
            margin=dict(l=10, r=10, t=50, b=20),
            xaxis=dict(
                showgrid=True,
                gridcolor="#222222",
                zeroline=False,
                linecolor="#333333",
                tickfont=dict(color="#BDBDBD")
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#222222",
                zeroline=False,
                linecolor="#333333",
                tickfont=dict(color="#BDBDBD")
            )
        )
            fig1.update_traces(
            marker_line_color="#111111",
            marker_line_width=1,
            opacity=1
        )
            attack_loss = (
                filtered_df.groupby("Attack_ID")["Financial Loss in Million  Doller"]
                .sum()
                .reset_index()
            )
            st.plotly_chart(fig1,use_container_width=True,key="country_chart")
            st.markdown("---")
            fig2 = px.sunburst(
            filtered_df,
            path=["Attack Source", "Attack_ID"],
            values="Financial Loss in Million  Doller",
            title="Financial Loss by Attack Source & Attack Type",
            color="Financial Loss in Million  Doller",
            color_continuous_scale=[
                    "#102542",
                    "#1E3A5F",
                    "#2F5D8C",
                    "#4F81BD",
                    "#A7C7E7"
                ]  
        )
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                title_font=dict(color="#FFD700", size=22),
                margin=dict(l=10, r=10, t=50, b=10)
            )

            st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("---")

            
            fig3 = px.treemap(
                filtered_df,
                path=["Security Vulnerability Type"],
                title="Security Vulnerability Type"
            )
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                title_font_color="white",
                title_font=dict(color="#FFD700",size=22),
                height=300,
                margin=dict(l=10, r=10, t=40, b=10),
                coloraxis_colorbar=dict(thickness=12,len=0.7)
                
            )

            fig3.update_xaxes(
                showgrid=False,
                zeroline=False
            )

            fig3.update_yaxes(
                 title_font=dict(color="white"),
                tickfont=dict(color="white"),
                automargin=True,
                ticklabelposition="outside",
                showgrid=False,
                zeroline=False   )
            fig3 = px.treemap(
                filtered_df,
                path=["Security Vulnerability Type"],
                title="Security Vulnerability Type"
            )
            fig3.update_layout(
                paper_bgcolor="#0B0B10",
                plot_bgcolor="#0B0B10",
                font_color="white",
                title_font_color="white",
                title_font=dict(color="#FFD700",size=22),
                height=400,
                margin=dict(l=10, r=10, t=40, b=10),
                coloraxis_colorbar=dict(thickness=12,len=0.7)
                
            )

            fig3.update_xaxes(
                showgrid=False,
                zeroline=False
            )

            fig3.update_yaxes(
                 title_font=dict(color="white"),
                tickfont=dict(color="white"),
                automargin=True,
                ticklabelposition="outside",
                showgrid=False,
                zeroline=False   )
            fig3.update_traces(
            textfont=dict(size=18, color="black",
            )
)
            st.plotly_chart(fig3,use_container_width=True,key="treemap_chart")
            st.markdown("---")

elif page == "📊 Attack Analytics":

            st.title("📊 Attack Analytics")
            # Graph 1
            attack_source = (
                filtered_df.groupby("Attack Source")["Financial Loss in Million  Doller"]
                .sum()
                .reset_index()
            )
            fig4 = px.bar(
                attack_source,
                x="Attack Source",
                y="Financial Loss in Million  Doller",
                color="Attack Source",
                title="Total Financial Loss by Attack Source"
            )
            fig4.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0B0B10",
                plot_bgcolor="#0B0B10",
                font_color="white",
                title_font=dict(color="#FFD700",size=22),
                margin=dict(l=0, r=0, t=50, b=0)
            )
            fig4.update_xaxes(
                showgrid=False,
                zeroline=False
            )
            fig4.update_yaxes(
                showgrid=False,
                zeroline=False)
            st.plotly_chart(fig4, use_container_width=True,key="attack_source_chart")
            st.markdown("---")
            # Graph 2
            yearly = (
                filtered_df.groupby("Year")
                .agg({
                    "Financial Loss in Million  Doller":"sum",
                    "Number of Affected Users":"sum"
                })
                .reset_index()
            )
            # dual axis figure
            fig5 = make_subplots(specs=[[{"secondary_y": True}]])
            # Financial Loss line
            fig5.add_trace(
                go.Scatter(
                    x=yearly["Year"],
                    y=yearly["Financial Loss in Million  Doller"],
                    name="Total_Financial_loss",
                    mode="lines+markers",
                    line=dict(color="yellow")
                ),
                secondary_y=False
            )
            # Affected Users line
            fig5.add_trace(
                go.Scatter(
                    x=yearly["Year"],
                    y=yearly["Number of Affected Users"],
                    name="Total_affected_user",
                    mode="lines+markers",
                    line=dict(color="red")
                ),
                secondary_y=True
            )
            yearly = (
                filtered_df.groupby("Year")
                .agg({
                    "Financial Loss in Million  Doller":"sum",
                    "Number of Affected Users":"sum"
                })
                .reset_index()
            )
            # dual axis figure
            fig5 = make_subplots(specs=[[{"secondary_y": True}]])
            # Financial Loss line
            fig5.add_trace(
                go.Scatter(
                    x=yearly["Year"],
                    y=yearly["Financial Loss in Million  Doller"],
                    name="Total_Financial_loss",
                    mode="lines+markers",
                    line=dict(color="yellow")
                ),
                secondary_y=False
            )
            # Affected Users line
            fig5.add_trace(
                go.Scatter(
                    x=yearly["Year"],
                    y=yearly["Number of Affected Users"],
                    name="Total_affected_user",
                    mode="lines+markers",
                    line=dict(color="red")
                ),
                secondary_y=True
            )
            fig5.update_layout(
            template="plotly_dark",
            title=dict(
            text="Financial Loss vs Affected Users by Year",
            x=0.5,
            xanchor="center",
            font=dict(color="#FFD700", size=22)
            ),
            paper_bgcolor="#0B0B10",
            plot_bgcolor="#0B0B10",
            font_color="white",
            height=500,
            margin=dict(l=20, r=20, t=80, b=20),
            legend=dict(
            x=1.02,
            y=1,
            bgcolor="rgba(0,0,0,0)"
            )
            )
            fig5.update_xaxes(
                showgrid=False,
                zeroline=False
            )
            fig5.update_yaxes(
                showgrid=False,
                zeroline=False)
            # layout settings
            st.plotly_chart(fig5, use_container_width=True,key="yearly_chart")
            st.markdown("---")
            # Graph 3
            heatmap_data = filtered_df.pivot_table(
            index="Attack Source",
            columns="Year",
            values="Attack_ID",
            aggfunc="count",
            fill_value=0
        )

            fig6 = px.imshow(
            heatmap_data,
            text_auto=True,
            color_continuous_scale="Reds",
            title="Cyber Attack Trend by Source and Year"
        )

            fig6.update_layout(
            paper_bgcolor="#0B0B10",
            plot_bgcolor="#0B0B10",
            font_color="white",
            title_font=dict(color="#FF0040", size=22)
        )
            st.plotly_chart(fig6, use_container_width=True)
            st.markdown("---")
            
            
elif page == "📈 Industry Analytics":
            st.subheader("📈 Industry Analytics")
            # Graph 1 - Financial Loss by Target Industry
            industry_loss = (
                filtered_df.groupby("Target Industry")["Financial Loss in Million  Doller"]
                .sum()
                .reset_index()
            )
            fig7 = px.bar(
                industry_loss,
                x="Target Industry",
                y="Financial Loss in Million  Doller",
                color="Target Industry",
                title="Financial Loss by Target Industry"
            )
            fig7.update_layout(
                paper_bgcolor="#0B0B10",
                plot_bgcolor="#0B0B10",
                font_color="white",
                margin=dict(l=0, r=0, t=30, b=0),
                title_font=dict(color="#FFD700",size=22)
            )
            fig7.update_xaxes(
                showgrid=False,
                zeroline=False
            )
            fig7.update_yaxes(
                showgrid=False,
                zeroline=False)
            st.plotly_chart(fig7, use_container_width=True)
            st.markdown("---")
            # Graph 2 - Defence Mechanism Used
            defence = (
                filtered_df["Defense Mechanism Used"]
                .value_counts()
                .reset_index()
            )
            # Defense Mechanism Used
            defence = (
                filtered_df["Defense Mechanism Used"]
                .value_counts()
                .reset_index()
            )
            defence.columns = ["Defense Mechanism Used", "Count"]

            fig8 = px.bar_polar(
                defence,
                r="Count",
                theta="Defense Mechanism Used",
                color="Count",
            
                color_continuous_scale=[
                "#6A00F4",
                "#8E2DE2",
                "#B5179E",
                "#E9C46A",
                "#FFD60A"
            ],
            
                title="Defense Mechanism Used"
            )

            fig8.update_layout(
                  height=500,
                paper_bgcolor="#0B0B10",
                plot_bgcolor="#0B0B10",
                font_color="white",
                title_font=dict(color="#FFD700", size=22),
                coloraxis_showscale=False,
                polar=dict(
                    bgcolor="#0B0B10",
                    radialaxis=dict(
                        showgrid=True,
                        gridcolor="#333333",
                        tickfont=dict(color="white")
                    ),
                    angularaxis=dict(
                        tickfont=dict(color="white")
                    )
                )
            )
            st.plotly_chart(fig8,use_container_width=True)
            st.markdown("---")
            # Graph 3 - Target Industry Distribution
            fig9 = px.treemap(
                filtered_df,
                path=["Target Industry"],
                title="Target Industry Distribution"
            )
            fig9.update_layout(
                paper_bgcolor="#0B0B10",
                plot_bgcolor="#0B0B10",
                font_color="white",
                margin=dict(l=0, r=0, t=50, b=0),
                title_font=dict(color="#FFD700",size=22)
            )
            fig9.update_traces(
            textfont=dict(
            color="black",
            size=18
    )
)
            fig9.update_xaxes(
                showgrid=False,
                zeroline=False
            )

            fig9.update_yaxes(
                showgrid=False,
                zeroline=False)

            st.plotly_chart(fig9, use_container_width=True)
            st.markdown("---")

elif page == "💡 Insights":

            st.subheader("💡 Cyber Crime Insights")

            col1, col2 = st.columns(2)

            with col1:
                st.success(f"🌍 Country with Highest Financial Loss: {filtered_df.groupby('Country')['Financial Loss in Million  Doller'].sum().idxmax()}")

                st.info(f"🏭 Most Targeted Industry: {filtered_df['Target Industry'].mode()[0]}")

                st.warning(f"⚔️ Most Common Attack Source: {filtered_df['Attack Source'].mode()[0]}")

            with col2:
                st.success(f"🔓 Most Common Vulnerability: {filtered_df['Security Vulnerability Type'].mode()[0]}")

                st.info(f"🛡️ Most Used Defense Mechanism: {filtered_df['Defense Mechanism Used'].mode()[0]}")

                st.warning(f"📌 Total Cyber Attacks: {len(filtered_df)}")

            st.markdown("---")

            st.subheader("📋 Key Findings")


            st.write(f"✅ Total Cyber Attacks: {len(filtered_df)}")

            st.write(f"✅ Highest Financial Loss Country: {filtered_df.groupby('Country')['Financial Loss in Million  Doller'].sum().idxmax()}")

            st.write(f"✅ Most Targeted Industry: {filtered_df['Target Industry'].mode()[0]}")

            st.write(f"✅ Most Common Attack Source: {filtered_df['Attack Source'].mode()[0]}")

            st.write(f"✅ Most Used Defense Mechanism: {filtered_df['Defense Mechanism Used'].mode()[0]}")
elif page == "🧹 Data Cleaning":
            st.title("🧹 Data Cleaning")
            st.subheader("🧹 Data Cleaning")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Rows", df.shape[0])

            with c2:
                st.metric("Columns", df.shape[1])

            with c3:
                st.metric("Missing Values", df.isnull().sum().sum())

            with c4:
                st.metric("Duplicates", df.duplicated().sum())

            st.markdown("---")

            st.subheader("📄 Data Preview")
            rows = st.slider("Rows to Preview", 5, 50, 10)
            st.dataframe(filtered_df.head(rows), use_container_width=True)
            st.markdown("---")

            st.subheader("📥 Export Filtered Data")

            csv = filtered_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="Cyber_Crime_Filtered_Data.csv",
                mime="text/csv"
            )

            csv=filtered_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "📥 Download Filtered Data",
                csv,
                "Cyber_Crime_Data.csv",
                "text/csv"
            )
            st.write("Dataset Shape :",df.shape)
            st.write("Dataset Columns")
            st.write(df.columns.tolist())

elif page == "ℹ️ About":

            st.title("ℹ️ About Cyber Crime Analysis Dashboard")

            st.markdown("""
            ### 📌 Project Overview
            The Cyber Crime Analysis Dashboard is developed using **Python, Streamlit, Pandas, and Plotly**. It analyzes cyber attack data to identify attack trends, financial losses, target industries, and security vulnerabilities through interactive visualizations.

            ### 🎯 Objectives
            - Analyze cyber crime incidents across different countries.
            - Identify the most targeted industries.
            - Compare financial losses caused by different attack types.
            - Analyze attack sources and security vulnerabilities.
            - Support data-driven cybersecurity decisions.

            ### 🛠️ Technologies Used
            - Python
            - Streamlit
            - Pandas
            - Plotly
            - VS Code

            ### 📂 Dataset Includes
            - Country
            - Year
            - Attack ID
            - Attack Source
            - Target Industry
            - Financial Loss
            - Number of Affected Users
            - Security Vulnerability Type
            - Defense Mechanism Used
            - Incident Resolution Time

            ### ✨ Dashboard Features
            ✅ Data Cleaning

            ✅ Interactive Filters

            ✅ KPI Dashboard

            ✅ Analytics Charts

            ✅ Industry Analysis

            ✅ Cyber Crime Insights

            ### 👨‍💻 Developed By
            **Lovepreet Kaur**

            **B.Tech (AI & ML)**
            """)
elif page == "🌍 Hotspot Map":
            st.title("🌍 Cyber Crime Hotspot Map")

            country_map = (
                filtered_df.groupby("Country")
                .agg({
                    "Financial Loss in Million  Doller": "sum",
                    "Attack_ID": "count"
                })
                .reset_index()
            )

            country_map.rename(columns={"Attack_ID": "Total Attacks"}, inplace=True)

            fig = px.scatter_geo(
                country_map,
                locations="Country",
                locationmode="country names",
                size="Total Attacks",
                color="Total Attacks",
                hover_name="Country",
                hover_data={
                    "Financial Loss in Million  Doller": True,
                    "Total Attacks": True
                },
                color_continuous_scale="Reds",
                projection="natural earth",
                title="Cyber Attack Hotspot Map"
            )

            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0B0B10",
                plot_bgcolor="#0B0B10",
                font_color="white",
                title_font=dict(color="#FFD700", size=22),
                title_x=0.5,
                margin=dict(l=0, r=0, t=60, b=0),

                geo=dict(
                bgcolor="white",
                showframe=False,
                showcoastlines=True,
                coastlinecolor="#666666",
                showcountries=True,
                countrycolor="#666666",
                showland=True,
                landcolor="#F5F5F5",
                showocean=True,
                oceancolor="#DCEEFF"
)
            )
            st.plotly_chart(fig, use_container_width=True)

            st.info("The map highlights countries with higher cyber attack incidents based on the selected filters.")