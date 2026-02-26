import plotly.express as px
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Tech Job Market Intelligence",
    layout="wide"
)

plt.style.use("dark_background")

# ---------------- TITLE ----------------
st.title("📊 Tech Job Market Intelligence Platform")
st.markdown("Analyze hiring trends, salaries and skills demand")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("jobs_dataset.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🔎 Filters")

location_filter = st.sidebar.multiselect(
    "📍 Location",
    df["location"].unique(),
    default=df["location"].unique()
)

experience_filter = st.sidebar.multiselect(
    "🧠 Experience",
    df["experience"].unique(),
    default=df["experience"].unique()
)

role_filter = st.sidebar.multiselect(
    "💼 Job Role",
    df["title"].unique(),
    default=df["title"].unique()
)

# ---------------- FILTERED DATA ----------------
filtered_df = df[
    (df["location"].isin(location_filter)) &
    (df["experience"].isin(experience_filter)) &
    (df["title"].isin(role_filter))
]

if filtered_df.empty:
    st.warning("No data available for selected filters")
    st.stop()

# ---------------- KPI SECTION ----------------
st.markdown("---")
st.subheader("📌 Market Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Jobs", len(filtered_df))
col2.metric("Average Salary", f"₹ {int(filtered_df['salary'].mean()):,}")
col3.metric(
    "Top City",
    filtered_df["location"].value_counts().idxmax()
)

# ---------------- CITY COMPARISON ----------------
st.markdown("---")
st.subheader("🏙️ City Salary Comparison")

city1 = st.selectbox("Select First City", df["location"].unique())
city2 = st.selectbox("Select Second City", df["location"].unique())

avg1 = df[df["location"] == city1]["salary"].mean()
avg2 = df[df["location"] == city2]["salary"].mean()

c1, c2 = st.columns(2)
c1.metric(city1, f"₹ {int(avg1):,}")
c2.metric(city2, f"₹ {int(avg2):,}")

# ---------------- SALARY BY LOCATION GRAPH ----------------

st.markdown("---")
st.subheader("💰 Salary Distribution by Location")

salary_location = (
    filtered_df.groupby("location")["salary"]
    .mean()
    .reset_index()
)

fig = px.bar(
    salary_location,
    x="location",
    y="salary",
    color="salary",
    text="salary",
    title="Average Salary by City"
)

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

st.plotly_chart(fig, use_container_width=True)
# ---------------- SKILL DEMAND GRAPH ----------------

st.subheader("🔥 Top Skill Demand")

# Split skills column
skills_series = filtered_df['skills'].dropna().str.split(',')

# Flatten skills
all_skills = skills_series.explode().str.strip()

# Count skills
top_skills = all_skills.value_counts().head(10).reset_index()
top_skills.columns = ['Skill', 'Demand']

# Plotly Interactive Chart
fig_skills = px.bar(
    top_skills,
    x="Demand",
    y="Skill",
    orientation="h",
    text="Demand",
    title="Most In-Demand Skills",
)

fig_skills.update_layout(
    height=500,
    yaxis=dict(categoryorder="total ascending"),
    template="plotly_white"
)

st.plotly_chart(fig_skills, use_container_width=True)

# ---------------- AI MARKET SUMMARY ----------------
st.markdown("---")
st.subheader("🤖 AI Market Intelligence Summary")

# Most demanded role
top_role = filtered_df["title"].value_counts().idxmax()

role_salary = int(
    filtered_df[
        filtered_df["title"] == top_role
    ]["salary"].mean()
)

# Skill analysis
skills_series = (
    filtered_df["skills"]
    .str.split(", ")
    .explode()
)

top_skill = skills_series.value_counts().idxmax()

skill_jobs = filtered_df[
    filtered_df["skills"].str.contains(top_skill, na=False)
]

skill_salary = int(skill_jobs["salary"].mean())

top_city = filtered_df["location"].value_counts().idxmax()

summary = f"""
📍 Hiring demand is highest in **{top_city}**.

💼 The most demanded role is **{top_role}**,\n
with an average salary of **₹ {role_salary:,}**.

🚀 Professionals skilled in **{top_skill}**
earn approximately **₹ {skill_salary:,}** on average.

This indicates strong employer preference toward
specialized technical capabilities driving compensation growth.
"""

st.success(summary)

# ---------------- SALARY PREDICTION ----------------
st.markdown("---")
st.subheader("🔮 Salary Prediction")

exp_map = {
    "0-2 Years":1,
    "2-5 Years":2,
    "5-8 Years":3,
    "8+ Years":4
}

df["exp_encoded"] = df["experience"].map(exp_map)

role_encoder = LabelEncoder()
df["role_encoded"] = role_encoder.fit_transform(df["title"])

X = df[["exp_encoded","role_encoded"]]
y = df["salary"]

model = LinearRegression()
model.fit(X,y)

selected_exp = st.selectbox(
    "Select Experience",
    df["experience"].unique()
)

selected_role = st.selectbox(
    "Select Role",
    df["title"].unique()
)

pred_salary = model.predict([[
    exp_map[selected_exp],
    role_encoder.transform([selected_role])[0]
]])[0]

st.metric("Predicted Salary", f"₹ {int(pred_salary):,}")

# ---------------- DOWNLOAD BUTTON ----------------
st.markdown("---")

st.download_button(
    "⬇ Download Filtered Data",
    filtered_df.to_csv(index=False),
    file_name="filtered_jobs.csv",
    mime="text/csv"
)