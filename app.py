import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Global Childhood Vaccination Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/Cleaned_WUENIC.csv")
    return df

df = load_data()

# ---------------------------------------------------
# Dashboard Title
# ---------------------------------------------------
st.title("🌍 Global Childhood Vaccination Dashboard")

st.markdown("""
Explore global childhood **DTP3 vaccination coverage** between **2015 and 2025**
using the **WHO/UNICEF Estimates of National Immunization Coverage (WUENIC)**.
""")

with st.expander("About this Dashboard"):
    st.markdown("""
### About this Dashboard

This dashboard analyses **DTP3 vaccination coverage**, a key indicator used by the
World Health Organization (WHO) and UNICEF to monitor the performance of routine
childhood immunisation programmes worldwide.

#### What is DTP3?

DTP3 refers to the **third dose** of the vaccine that protects against:

- Diphtheria
- Tetanus
- Pertussis (Whooping Cough)

#### Who does it apply to?

DTP3 coverage measures the percentage of **surviving infants (approximately one year old)**
who have received all three recommended doses of the DTP vaccine.

#### Why is DTP3 important?

DTP3 coverage is widely recognised as one of the best indicators of the strength and
accessibility of a country's routine immunisation programme. High coverage helps reduce
the risk of disease outbreaks and contributes to improved child health.

**Data Source:** WHO/UNICEF Estimates of National Immunization Coverage (WUENIC).
""")

st.divider()
# ---------------------------------------------------
# Dashboard KPIs
# ---------------------------------------------------
st.title("Overall Analysis")


st.info("""Vaccination coverage is the percentage of the target population that received the recommended DTP3 vaccine. The **average coverage** represents the mean vaccination coverage across all **201 countries** in the dataset for the selected year.

Higher coverage indicates that a greater proportion of children are protected against diphtheria, tetanus, and pertussis (whooping cough).
""")


countries = df["NAME"].nunique()

coverage_2015 = df[df["YEAR"] == 2015]
coverage_2025 = df[df["YEAR"] == 2025]

average_coverage_2015 = (
    coverage_2015["COVERAGE"]
    .mean()
)

average_coverage_2025 = (
    coverage_2025["COVERAGE"]
    .mean()
)

coverage_change = (
    average_coverage_2025 
    - average_coverage_2015
)


# KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🌍 Countries",
        countries
    )

with col2:
    st.metric(
        "Average Coverage (2015)",
        f"{average_coverage_2015:.1f}%"
    )

with col3:
    st.metric(
        "Average Coverage (2025)",
        f"{average_coverage_2025:.1f}%",
        delta=f"{coverage_change:+.1f} pp"
    )



st.warning("""
The average DTP3 vaccination coverage decreased from **88.0% in 2015** to **86.5% in 2025**,
representing a decline of **1.5 percentage points**.

This indicates that, on average, countries reported lower childhood DTP3 vaccination
coverage in 2025 than in 2015, suggesting a reduction in routine immunisation coverage
over the study period.
""")

st.divider()

# ---------------------------------------------------
# WHO / IA2030 Target
# ---------------------------------------------------



meeting_2015 = (coverage_2015["COVERAGE"] >= 90).sum()
meeting_2025 = (coverage_2025["COVERAGE"] >= 90).sum()

below_2015 = (coverage_2015["COVERAGE"] < 90).sum()
below_2025 = (coverage_2025["COVERAGE"] < 90).sum()

change = meeting_2025 - meeting_2015


st.title("DTP3 Target")

# Explanation BEFORE graph
st.info("""The WHO and UNICEF Immunization Agenda 2030 (IA2030) aims for every country to achieve
**at least 90% national coverage** of the third dose of the diphtheria, tetanus and
pertussis (DTP3) vaccine by 2030.

DTP3 coverage refers to the percentage of surviving infants who received three doses
of the diphtheria, tetanus, and pertussis-containing vaccine in a given year.

Source: [WHO DTP3 Immunization Coverage Indicator](https://www.who.int/data/gho/indicator-metadata-registry/imr-details/7791?utm_source=)

The chart below compares how many countries met this target in 2015 and 2025.
""")


# Target KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "2015 ≥90%",
        meeting_2015
    )

with col2:
    st.metric(
        "2025 ≥90%",
        meeting_2025
    )

with col3:
    st.metric(
        "Change",
        f"{change:+}"
    )








# Graph
who_df = pd.DataFrame({
    "Year": ["2015", "2015", "2025", "2025"],
    "Category": [
        "Meeting ≥90%",
        "Below 90%",
        "Meeting ≥90%",
        "Below 90%"
    ],
    "Countries": [
        meeting_2015,
        below_2015,
        meeting_2025,
        below_2025
    ]
})


fig = px.bar(
    who_df,
    x="Year",
    y="Countries",
    color="Category",
    barmode="group",
    text="Countries",
    template="plotly_white"
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    title="Countries Meeting the WHO/UNICEF IA2030 DTP3 Target",
    title_x=0.5,
    xaxis_title="",
    yaxis_title="Number of Countries"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# Insight message
if change > 0:
    st.success(
        f"{change} more countries met the WHO/UNICEF IA2030 target in 2025 than in 2015."
    )

elif change < 0:
    st.warning(
        f"{abs(change)} fewer countries met the WHO/UNICEF IA2030 target in 2025 than in 2015."
    )

else:
    st.info(
        "The number of countries meeting the WHO/UNICEF IA2030 target remained unchanged."
    )


st.divider()



# ---------------------------------------------------
# Most & Least Improved Countries
# ---------------------------------------------------

st.title("Change in Coverage (2015–2025)")

st.info("""
The chart on the **left** highlights the **10 countries that experienced the largest increase**
in DTP3 vaccination coverage between **2015 and 2025**.

The chart on the **right** highlights the **10 countries that experienced the largest decrease**
in DTP3 vaccination coverage over the same period.

""")

# Coverage in 2015
coverage_2015 = (
    df[df["YEAR"] == 2015][["NAME", "COVERAGE"]]
    .rename(columns={"COVERAGE": "Coverage_2015"})
)

# Coverage in 2025
coverage_2025 = (
    df[df["YEAR"] == 2025][["NAME", "COVERAGE"]]
    .rename(columns={"COVERAGE": "Coverage_2025"})
)

# Merge together
improvement_df = coverage_2015.merge(
    coverage_2025,
    on="NAME"
)

# Calculate improvement
improvement_df["Improvement"] = (
    improvement_df["Coverage_2025"]
    - improvement_df["Coverage_2015"]
)

# Sort once
improvement_df = improvement_df.sort_values("Improvement")


# Function to plot the chart
def plot_improvement(data, title):
    fig = px.bar(
        data,
        x="Improvement",
        y="NAME",
        orientation="h",
        text="Improvement",
        template="plotly_white"
    )

    fig.update_layout(
        title=title,
        xaxis_title="Improvement (Percentage Points)",
        yaxis_title="",
        title_x=0.5
    )

    fig.update_traces(textposition="outside")

    fig.update_yaxes(autorange="reversed")

    st.plotly_chart(fig, use_container_width=True)




# Bottom 10
bottom10 = improvement_df.head(10)

# Top 10
top10 = improvement_df.tail(10).sort_values(
    "Improvement",
    ascending=False
)

# Display charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("10 Most Improved Countries")
    plot_improvement(top10, "10 Most Improved Countries")

with col2:
    st.subheader("10 Least Improved Countries")
    plot_improvement(bottom10, "10 Least Improved Countries")

st.warning("""
**Ukraine** recorded the largest improvement in DTP3 vaccination coverage, increasing by **71 percentage points** between **2015 and 2025**.

**Kazakhstan** experienced the largest decline in DTP3 vaccination coverage, decreasing by **39 percentage points** over the same period.

These results highlight considerable variation in childhood vaccination trends across countries, with some nations making substantial progress while others experienced significant declines in coverage.
""")

# ---------------------------------------------------
# Dashboard Controls
# ---------------------------------------------------

st.title("Comparison across years")

control_col1, control_col2 = st.columns(2)

country_options = sorted(df["NAME"].unique())

selected_country = control_col1.selectbox(
    "🌍 Country",
    country_options,
    index=country_options.index("South Africa") if "South Africa" in country_options else 0
)

comparison_options = ["None", "Global Average"] + country_options

selected_comparison = control_col2.selectbox(
    "Compare With",
    comparison_options,
    index=1   # Global Average by default
)

st.divider()

# ---------------------------------------------------
# Vaccination Trend
# ---------------------------------------------------


fig = go.Figure()

# Primary country
country_df = (
    df[df["NAME"] == selected_country]
    .sort_values("YEAR")
)

fig.add_trace(
    go.Scatter(
        x=country_df["YEAR"],
        y=country_df["COVERAGE"],
        mode="lines+markers",
        name=selected_country
    )
)

# Comparison
if selected_comparison == "Global Average":

    global_df = (
        df.groupby("YEAR", as_index=False)["COVERAGE"]
        .mean()
    )

    fig.add_trace(
        go.Scatter(
            x=global_df["YEAR"],
            y=global_df["COVERAGE"],
            mode="lines+markers",
            name="Global Average"
        )
    )

elif selected_comparison != "None":

    comparison_df = (
        df[df["NAME"] == selected_comparison]
        .sort_values("YEAR")
    )

    fig.add_trace(
        go.Scatter(
            x=comparison_df["YEAR"],
            y=comparison_df["COVERAGE"],
            mode="lines+markers",
            name=selected_comparison
        )
    )

fig.update_layout(
    title=f"{selected_country} Vaccination Coverage",
    xaxis_title="Year",
    yaxis_title="Coverage (%)",
    hovermode="x unified",
    template="plotly_white",
    title_x=0.5,
    height=550
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# 2030 Projection
# ---------------------------------------------------

st.title("Projection to 2030")

st.info("""
A simple **linear trend** was fitted to each country's DTP3 vaccination coverage
between **2015 and 2025**. The trend was then projected to **2030**.

This is **not a forecast**. It assumes that each country's historical trend continues
unchanged and does not account for future policy changes, disease outbreaks, conflicts,
or vaccination campaigns.
""")

projection_results = []

for country in df["NAME"].unique():

    country_df = (
        df[df["NAME"] == country]
        .sort_values("YEAR")
    )

    # Fit linear trend
    slope, intercept = np.polyfit(
        country_df["YEAR"],
        country_df["COVERAGE"],
        1
    )

    # Predict 2030
    projected = slope * 2030 + intercept

    # Coverage cannot be below 0 or above 100
    projected = max(0, min(100, projected))

    projection_results.append(
        {
            "Country": country,
            "Projected_2030": projected
        }
    )

projection_df = pd.DataFrame(projection_results)

projected_meeting = (
    projection_df["Projected_2030"] >= 90
).sum()

change = projected_meeting - meeting_2025

col1, col2, col3 = st.columns(3)

col1.metric(
    "Countries ≥90% (2025)",
    meeting_2025
)

col2.metric(
    "Projected ≥90% (2030)",
    projected_meeting
)

col3.metric(
    "Projected Change",
    f"{change:+}"
)

projection_chart = pd.DataFrame({
    "Year": ["2015", "2025", "2030 (Projected)"],
    "Countries Meeting Target": [
        meeting_2015,
        meeting_2025,
        projected_meeting
    ]
})

fig = px.bar(
    projection_chart,
    x="Year",
    y="Countries Meeting Target",
    text="Countries Meeting Target",
    template="plotly_white",
    color="Year"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    title="Countries Expected to Meet the WHO/UNICEF 90% DTP3 Target",
    title_x=0.5,
    showlegend=False,
    yaxis_title="Number of Countries"
)

st.plotly_chart(fig, use_container_width=True)

st.warning(f"""
If each country's **2015–2025 vaccination trend** continues unchanged,
approximately **{projected_meeting} countries** are projected to achieve
the WHO/UNICEF IA2030 target of **90% DTP3 coverage** by **2030**.

This represents a projected change of **{change:+} countries** compared with 2025.

*This projection is based on a simple linear trend and should be interpreted
as an indication of the current trajectory rather than a prediction.*
""")

# ---------------------------------------------------
# Data Explorer
# ---------------------------------------------------

st.subheader("Data Explorer")

# Create two columns for the filters
filter_col1, filter_col2 = st.columns(2)

# Country filter
countries = ["All Countries"] + sorted(df["NAME"].unique())

selected_country = filter_col1.selectbox(
    "Select Country",
    countries
)

# Year filter
years = ["All Years"] + sorted(df["YEAR"].unique())

selected_year = filter_col2.selectbox(
    "Select Year",
    years
)

# Apply filters
filtered_df = df.copy()

if selected_country != "All Countries":
    filtered_df = filtered_df[
        filtered_df["NAME"] == selected_country
    ]

if selected_year != "All Years":
    filtered_df = filtered_df[
        filtered_df["YEAR"] == selected_year
    ]

st.dataframe(filtered_df, use_container_width=True)


st.divider()

st.caption("""
**Source:** WHO/UNICEF Estimates of National Immunization Coverage (WUENIC).

**WHO/UNICEF Immunization Agenda 2030 (IA2030):**
The global target is for every country to achieve at least **90% national DTP3 coverage by 2030**.
""")
