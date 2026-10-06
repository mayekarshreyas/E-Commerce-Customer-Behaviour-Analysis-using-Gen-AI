import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

df = pd.read_csv("E-commerce Customer Behavior Dataset.csv")

# ======================================================
# SIDEBAR FILTERS
# ======================================================

st.sidebar.header("Dashboard Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["City"].dropna().unique()),
    default=sorted(df["City"].dropna().unique())
)

membership_filter = st.sidebar.multiselect(
    "Select Membership Type",
    options=sorted(df["Membership Type"].dropna().unique()),
    default=sorted(df["Membership Type"].dropna().unique())
)

satisfaction_filter = st.sidebar.multiselect(
    "Select Satisfaction Level",
    options=sorted(
        df["Satisfaction Level"]
        .dropna()
        .astype(str)
        .unique()
    ),
    default=sorted(
        df["Satisfaction Level"]
        .dropna()
        .astype(str)
        .unique()
    )
)

filtered_df = df[
    (df["City"].isin(city_filter))
    &
    (df["Membership Type"].isin(membership_filter))
    &
    (
        df["Satisfaction Level"]
        .astype(str)
        .isin(satisfaction_filter)
    )
]

# Download Button
st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ======================================================
# TITLE
# ======================================================

st.title("📊 Customer Analytics Dashboard")

# ======================================================
# KPI CALCULATIONS
# ======================================================

best_membership = (
    filtered_df.groupby("Membership Type")["Total Spend"]
    .sum()
    .idxmax()
)

highest_city = (
    filtered_df.groupby("City")["Total Spend"]
    .sum()
    .idxmax()
)

satisfaction_rate = (
    (filtered_df["Satisfaction Level"] == "Satisfied")
    .mean() * 100
)

# ======================================================
# KPI SECTION
# ======================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Customers",
    len(filtered_df)
)

col2.metric(
    "Total Revenue",
    f"${filtered_df['Total Spend'].sum():,.0f}"
)

col3.metric(
    "Average Spend",
    f"${filtered_df['Total Spend'].mean():.2f}"
)

col4.metric(
    "Average Rating",
    round(filtered_df["Average Rating"].mean(), 2)
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Best Membership Tier",
    best_membership
)

col6.metric(
    "Highest Spending City",
    highest_city
)

col7.metric(
    "Average Items Purchased",
    int(round(filtered_df["Items Purchased"].mean()))
)

col8.metric(
    "Satisfaction Rate",
    f"{satisfaction_rate:.1f}%"
)

# ======================================================
# TABS
# ======================================================

overview_tab, customer_tab, insight_tab = st.tabs(
    [
        "📊 Overview",
        "👥 Customer Analysis",
        "💡 Business Insights"
    ]
)

# ======================================================
# OVERVIEW TAB
# ======================================================

with overview_tab:

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        revenue_membership = (
            filtered_df.groupby("Membership Type")["Total Spend"]
            .sum()
            .reset_index()
        )

        fig1 = px.pie(
            revenue_membership,
            names="Membership Type",
            values="Total Spend",
            title="Revenue Contribution by Membership Type"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    with row1_col2:

        city_spend = (
            filtered_df.groupby("City")["Total Spend"]
            .mean()
            .reset_index()
            .sort_values(
                "Total Spend",
                ascending=False
            )
        )

        fig2 = px.bar(
            city_spend,
            x="City",
            y="Total Spend",
            title="Average Spending by City",
            text_auto=".0f"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:

        customer_dist = (
            filtered_df["Membership Type"]
            .value_counts()
            .reset_index()
        )

        customer_dist.columns = [
            "Membership Type",
            "Customer Count"
        ]

        fig3 = px.pie(
            customer_dist,
            names="Membership Type",
            values="Customer Count",
            hole=0.5,
            title="Customer Distribution by Membership Type"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with row2_col2:

        city_items = (
            filtered_df.groupby("City")["Items Purchased"]
            .mean()
            .round(0)
            .astype(int)
            .reset_index()
            .sort_values(
            "Items Purchased",
            ascending=False
            )
        )
        fig4 = px.bar(
            city_items,
            x="City",
            y="Items Purchased",
            title="Average Items Purchased by City",
            text_auto=True,
            color="Items Purchased"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
    )

    top_city_items = city_items.iloc[0]["City"]

    
# ======================================================
# CUSTOMER ANALYSIS TAB
# ======================================================

with customer_tab:

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:

        sat_dist = (
            filtered_df["Satisfaction Level"]
            .value_counts()
            .reset_index()
        )

        sat_dist.columns = [
            "Satisfaction Level",
            "Count"
        ]

        fig5 = px.pie(
            sat_dist,
            names="Satisfaction Level",
            values="Count",
            hole=0.4,
            title="Customer Satisfaction Distribution"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )

    with row1_col2:

        satisfaction_membership = pd.crosstab(
            filtered_df["Membership Type"],
            filtered_df["Satisfaction Level"]
        )

        fig6 = px.bar(
            satisfaction_membership,
            barmode="stack",
            title="Satisfaction Level by Membership Type"
        )

        st.plotly_chart(
            fig6,
            use_container_width=True
        )

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:

        rating_membership = (
            filtered_df.groupby("Membership Type")
            ["Average Rating"]
            .mean()
            .reset_index()
        )

        fig7 = px.bar(
            rating_membership,
            x="Membership Type",
            y="Average Rating",
            title="Average Rating by Membership Type",
            text_auto=".1f"
        )

        st.plotly_chart(
            fig7,
            use_container_width=True
        )

    with row2_col2:

        rating_city = (
            filtered_df.groupby("City")
            ["Average Rating"]
            .mean()
            .reset_index()
            .sort_values(
                "Average Rating",
                ascending=False
            )
        )

        fig8 = px.bar(
            rating_city,
            x="City",
            y="Average Rating",
            title="Average Rating by City",
            text_auto=".1f"
        )

        st.plotly_chart(
            fig8,
            use_container_width=True
        )

# ======================================================
# BUSINESS INSIGHTS TAB
# ======================================================

with insight_tab:

    st.subheader("Top 10 Customers by Spending")

    top_customers = (
        filtered_df.sort_values(
            "Total Spend",
            ascending=False
        )
        [
            [
                "Customer ID",
                "City",
                "Membership Type",
                "Total Spend",
                "Average Rating"
            ]
        ]
        .head(10)
    )

    st.dataframe(
        top_customers,
        use_container_width=True
    )

    st.subheader(
        "High Spending Customers Not Purchased Recently"
    )

    avg_spend = filtered_df["Total Spend"].mean()

    inactive_customers = filtered_df[
        (filtered_df["Total Spend"] > avg_spend)
        &
        (filtered_df["Days Since Last Purchase"] > 30)
    ][
        [
            "Customer ID",
            "Membership Type",
            "Total Spend",
            "Average Rating",
            "Days Since Last Purchase"
        ]
    ]

    st.dataframe(
        inactive_customers,
        use_container_width=True
    )

    st.subheader("Revenue Contribution by City")

    city_revenue = (
        filtered_df.groupby("City")
        ["Total Spend"]
        .sum()
        .reset_index()
    )

    city_revenue["Revenue %"] = (
        city_revenue["Total Spend"]
        /
        city_revenue["Total Spend"].sum()
        * 100
    ).round(2)

    st.dataframe(
        city_revenue,
        use_container_width=True
    )

    st.subheader("Membership Performance Summary")

    membership_summary = (
        filtered_df.groupby("Membership Type")
        .agg(
            {
                "Total Spend": "mean",
                "Average Rating": "mean",
                "Items Purchased": "mean"
            }
        )
        .round(2)
        .reset_index()
    )

    membership_summary.columns = [
        "Membership Type",
        "Average Spend",
        "Average Rating",
        "Average Items Purchased"
    ]

    st.dataframe(
        membership_summary,
        use_container_width=True
    )

    with st.expander("🎯 Actionable Insights"):

        st.markdown("""
        - Focus marketing efforts on the highest-spending city to maximize revenue.

        - Encourage customers to upgrade to the best-performing membership tier.

        - Improve engagement strategies for membership tiers with lower average ratings.

        - Increase customer satisfaction initiatives in lower-rated cities to improve overall customer experience.

        - Offer targeted promotions to customers with high spending potential.

        - Increase customer retention efforts for inactive high-value customers.
        """)