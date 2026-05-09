import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

DATA_URL = "https://media.githubusercontent.com/media/brandmorrissey/Virginia_Misdemeanor_Caseflow/refs/heads/Sankey-Plot/VirginiaMisdemeanors_Trimmed.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, low_memory=False)
    df.columns = df.columns.str.strip()
    df["OffenseMonth"] = pd.to_datetime(df["OffenseMonth"])
    return df

df = load_data()

st.title("Misdemeanors in Virginia District Courts, 2010-2023")

def clear_filters():
    st.session_state.offense = "All"
    st.session_state.crime = "All"
    st.session_state.jurisdiction = "All"
    st.session_state.offense_time = "All"
    st.session_state.crime_time = "All"
    st.session_state.jurisdiction_time = "All"

tab1, tab2 = st.tabs(["Charge Outcomes", "Charges Over Time"])

with tab1:
    st.button("Clear Filters", on_click=clear_filters)

    offense_options = ["All"] + sorted(df["OffenseCategory"].dropna().unique())

    offense = st.selectbox(
        "VCC Offense Category:",
        offense_options,
        key="offense"
    )

    crime_data = df.copy()
    if offense != "All":
        crime_data = crime_data[crime_data["OffenseCategory"] == offense]

    crime_options = ["All"] + sorted(crime_data["RevisedCrimeFamily"].dropna().unique())

    crime = st.selectbox(
        "VCC Specific Offense Type:",
        crime_options,
        key="crime"
    )

    jurisdiction = st.selectbox(
        "Select Jurisdiction:",
        ["All"] + sorted(df["Jurisdiction"].dropna().unique()),
        key="jurisdiction"
    )

    filtered = df.copy()

    if offense != "All":
        filtered = filtered[filtered["OffenseCategory"] == offense]

    if crime != "All":
        filtered = filtered[filtered["RevisedCrimeFamily"] == crime]

    if jurisdiction != "All":
        filtered = filtered[filtered["Jurisdiction"] == jurisdiction]
    
    st.metric("Cases in current selection", len(filtered))

if filtered.empty:
    st.warning("No cases match the current filters.")
    st.stop()
    
    filtered["Suspect Arrested"] = filtered["Arrested"].map({
        1: "Arrested",
        0: "Not Arrested"
    })

summary = (
    filtered
    .groupby(["OffenseCategory", "Suspect Arrested", "OutcomeCleaned"])
    .size()
    .reset_index(name="Number of Cases")
    .rename(columns={
        "OffenseCategory": "VCC Offense Category",
        "OutcomeCleaned": "Case Disposition"
    })
)

summary["Percent of Current Selection"] = (
    summary["Number of Cases"] / summary["Number of Cases"].sum() * 100
).round(2)

summary["Percent of Current Selection"] = (
    summary["Percent of Current Selection"].astype(str) + "%"
)

labels = pd.unique(
    pd.concat([
        summary["VCC Offense Category"],
        summary["Suspect Arrested"],
        summary["Case Disposition"]
    ])
).tolist()

label_to_id = {label: i for i, label in enumerate(labels)}

links1 = pd.DataFrame({
    "source": summary["VCC Offense Category"].map(label_to_id),
    "target": summary["Suspect Arrested"].map(label_to_id),
    "value": summary["Number of Cases"]
})

links2 = pd.DataFrame({
    "source": summary["Suspect Arrested"].map(label_to_id),
    "target": summary["Case Disposition"].map(label_to_id),
    "value": summary["Number of Cases"]
})

links = pd.concat([links1, links2], ignore_index=True)

sankey_fig = go.Figure(data=[go.Sankey(
    node=dict(label=labels),
    link=dict(
        source=links["source"],
        target=links["target"],
        value=links["value"]
    )
)])

st.plotly_chart(sankey_fig, width="stretch")

st.subheader("Summary Table")
st.dataframe(summary, width="stretch")

with tab2:
    st.button("Clear Filters", on_click=clear_filters, key="clear_time")

    offense_time_options = ["All"] + sorted(df["OffenseCategory"].dropna().unique())

    offense_time = st.selectbox(
        "VCC Offense Category:",
        offense_time_options,
        key="offense_time"
    )

    crime_time_data = df.copy()

    if offense_time != "All":
        crime_time_data = crime_time_data[
            crime_time_data["OffenseCategory"] == offense_time
        ]

    crime_time_options = ["All"] + sorted(
        crime_time_data["RevisedCrimeFamily"].dropna().unique()
    )

    crime_time = st.selectbox(
        "VCC Specific Offense Type:",
        crime_time_options,
        key="crime_time"
    )

    jurisdiction_time = st.selectbox(
        "Select Jurisdiction:",
        ["All"] + sorted(df["Jurisdiction"].dropna().unique()),
        key="jurisdiction_time"
    )

    filtered_time = df.copy()

    if offense_time != "All":
        filtered_time = filtered_time[
            filtered_time["OffenseCategory"] == offense_time
        ]

    if crime_time != "All":
        filtered_time = filtered_time[
            filtered_time["RevisedCrimeFamily"] == crime_time
        ]

    if jurisdiction_time != "All":
        filtered_time = filtered_time[
            filtered_time["Jurisdiction"] == jurisdiction_time
        ]

    counts = (
        filtered_time
        .groupby("OffenseMonth")
        .size()
        .reset_index(name="Number of Cases")
        .sort_values("OffenseMonth")
    )

    time_fig = px.line(
        counts,
        x="OffenseMonth",
        y="Number of Cases",
        markers=True,
        title="Charges Over Time"
    )

    st.plotly_chart(time_fig, width="stretch")
