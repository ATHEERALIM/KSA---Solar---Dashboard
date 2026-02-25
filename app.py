import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Saudi Solar Intelligence", page_icon="☀️", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 12px; border: 1px solid #374151; }
    </style>
    """, unsafe_allow_html=True)

try:
    #  تحميل البيانات وتنظيفها
    df = pd.read_csv('ksa_solar_dataset_2024_detailed.csv', encoding='cp1252')
    df.columns = df.columns.str.strip()
    df = df.dropna()

    city_col = 'City'
    data_col = 'GHI' if 'GHI' in df.columns else 'Latitude'

    with st.sidebar:
        st.header("⚙️ التحكم بالعرض")
        all_cities = df[city_col].unique()
        selected_cities = st.multiselect("اختر المدن للمقارنة", options=all_cities, default=all_cities)
        color_choice = st.selectbox("نمط الألوان", ["Oranges", "YlOrRd", "Viridis", "Hot"])
        st.write("---")
        st.info("هذا النظام يحلل بيانات الإشعاع الشمسي لعام 2024.")

    # 5. معالجة البيانات المختارة (Grouping)
    filtered_df = df[df[city_col].isin(selected_cities)]
    summary = filtered_df.groupby(city_col)[data_col].mean().reset_index().sort_values(by=data_col, ascending=False)

    # 6. العرض الرئيسي
    st.title("  منصة ذكاء الطاقة الشمسية - السعودية")
    st.markdown(f"**تحليل أداء: {data_col}** لكل منطقة مختارة")
    
    # بطاقات الإحصائيات (Metrics)
    m1, m2, m3 = st.columns(3)
    m1.metric("إجمالي المدن", len(summary))
    m2.metric("أعلى متوسط إشعاع", f"{round(summary[data_col].max(), 1)}")
    m3.metric("المتوسط العام للمناطق", f"{round(summary[data_col].mean(), 1)}")

    st.divider()

    # 7. الرسم البياني والجدول التفصيلي
    col_chart, col_table = st.columns([2, 1])

    with col_chart:
        fig = px.bar(summary, 
                     x=city_col, 
                     y=data_col, 
                     color=data_col,
                     text_auto='.1f',
                     color_continuous_scale=color_choice,
                     template="plotly_dark",
                     title=f"مقارنة متوسط {data_col} بين المناطق")
        
        # تحسين مظهر المحاور
        fig.update_layout(xaxis_title="المدينة", yaxis_title="القيمة المتوسطة")
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.markdown("**النتائج الرقمية**")
        st.dataframe(summary.style.background_gradient(cmap='YlOrRd'), use_container_width=True, hide_index=True)

except Exception as e:

    st.error(f"حدث خطأ في قراءة الأعمدة. تأكدي أن الملف يحتوي على عمود باسم 'City'. التفاصيل: {e}")
