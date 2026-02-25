import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Saudi Solar Intelligence", layout="wide")

st.markdown("""
    <style>
    .stMetric { 
        background-color: #1f2937; 
        padding: 18px; 
        border-radius: 8px; 
        border: 1px solid #374151; 
    }
    </style>
""", unsafe_allow_html=True)

try:
    df = pd.read_csv('ksa_solar_dataset_2024_detailed.csv', encoding='cp1252')
    df.columns = df.columns.str.strip()
    df = df.dropna()

    city_col = "City"
    data_col = "GHI" if "GHI" in df.columns else "Latitude"

    with st.sidebar:
        st.header("Filters")
        all_cities = df[city_col].unique()
        selected_cities = st.multiselect(
            "Select cities",
            options=all_cities,
            default=all_cities
        )
        color_choice = st.selectbox(
            "Color scale",
            ["Oranges", "YlOrRd", "Viridis", "Hot"]
        )

    filtered_df = df[df[city_col].isin(selected_cities)]

    summary = (
        filtered_df
        .groupby(city_col)[data_col]
        .mean()
        .reset_index()
        .sort_values(by=data_col, ascending=False)
    )

    summary["Investment Score (%)"] = round(
        (summary[data_col] - summary[data_col].min()) /
        (summary[data_col].max() - summary[data_col].min()) * 100,
        2
    )

    st.title("Saudi Solar Radiation Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Number of Cities", len(summary))
    col2.metric("Max Average Radiation", round(summary[data_col].max(), 2))
    col3.metric("Overall Mean", round(summary[data_col].mean(), 2))

    st.divider()

    if "Latitude" in df.columns and "GHI" in df.columns:
        correlation = df[["Latitude", "GHI"]].corr()

        fig_corr = px.imshow(
            correlation,
            text_auto=True,
            color_continuous_scale=color_choice
        )
        st.subheader("Correlation Analysis")
        st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()

    col_chart, col_table = st.columns([2, 1])

    with col_chart:
        fig = px.bar(
            summary,
            x=city_col,
            y=data_col,
            color=data_col,
            text_auto=".2f",
            color_continuous_scale=color_choice,
            template="plotly_dark"
        )
        fig.update_layout(
            xaxis_title="City",
            yaxis_title="Average Value"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.subheader("Summary Table")
        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:
    st.error(f"Data loading error: {e}")
