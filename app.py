import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import random

# ===== Page Configuration =====
st.set_page_config(page_title="Salary Predictor App💼", page_icon="💸", layout="centered")

# ===== Custom CSS for Styling =====
st.markdown("""
<style>
    body {
        background-color: #f4f6f9;
    }
    .main {
        background: linear-gradient(145deg, #e0e0e0, #ffffff);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    .css-1d391kg { background-color: #fff0;}
</style>
""", unsafe_allow_html=True)

# ===== Load Animation from URL =====
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie Animations
lottie_growth = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")

# ===== Load Model =====
model = joblib.load("rf_model_compressed.pkl")

# ===== Encodings =====
education_encoding = {"Enter Education": 0, "High School": 1, "Bachelor's": 2, "Master's": 3, "PhD": 4}
location_encoding = {"Enter Location": 0, "Rural": 1, "Suburban": 2, "Urban": 3}
job_title_encoding = {
    'Enter Job Title': 0, 'Clerk': 1, 'Customer Support': 2, 'Data Analyst': 3, 'Data Scientist': 4,
    'Director': 5, 'HR Manager': 6, 'Product Manager': 7, 'Software Engineer': 8, 'Technician': 9
}
gender_encoding = {'Male': 0, 'Female': 1}

# ===== City Cost-of-Living Multipliers (Example Data) =====
city_multipliers = {
    "Mumbai": 1.4,    # 40% higher cost than baseline (Pune)
    "Bangalore": 1.3,
    "Delhi": 1.35,
    "Hyderabad": 1.1,
    "Pune": 1.0,      # Baseline (1x)
    "Chennai": 1.15
}

# ===== Relocation Planner Function =====
def adjust_salary_by_city(salary, from_city, to_city):
    if from_city not in city_multipliers or to_city not in city_multipliers:
        return salary  # Fallback if city not in dataset
    return salary * (city_multipliers[to_city] / city_multipliers[from_city])

# ===== Motivational Quotes =====
quotes = [
    "🚀 'The future depends on what you do today.' – Mahatma Gandhi",
    "🌟 'Success usually comes to those who are too busy to be looking for it.' – Henry David Thoreau",
    "💡 'Don’t watch the clock; do what it does. Keep going.' – Sam Levenson",
    "🔥 'Opportunities don't happen, you create them.' – Chris Grosser",
    "🎯 'Your career is your business. It’s time for you to manage it as a CEO.' – Dorit Sher"
]

# ===== Header Section =====
if lottie_growth:
    st_lottie(lottie_growth, height=200, key="ai")
st.title("💼 Employee Salary Prediction Pro")
st.markdown("Enter employee details below to predict **realistic salary** based on market standards.")

# ===== Input Form Section =====
with st.form("input_form"):
    st.markdown("### 🔍 Enter Candidate Details")

    col1, col2, col3 = st.columns(3)
    with col1:
        education = st.selectbox("🎓 Education", list(education_encoding.keys()))
        job_title = st.selectbox("💼 Job Title", list(job_title_encoding.keys()))
    with col2:
        experience = st.slider("👨‍💼 Experience (Years)", 0, 40, 2)
        gender = st.radio("🧍 Gender", list(gender_encoding.keys()), horizontal=True)
    with col3:
        location = st.selectbox("📍 Work Location", list(location_encoding.keys()))
        age = st.slider("🎂 Age", 18, 65, 24)
        current_city = st.selectbox("🏙️ Current City", list(city_multipliers.keys()))  # New field

    growth_rate = st.slider("📈 Expected Annual Salary Growth Rate (%)", 0, 20, 7, help="Adjust the expected yearly salary increase rate for projection.")
    submitted = st.form_submit_button("🚀 Predict")

if submitted:
    missing_fields = []
    if education == "Enter Education":
        missing_fields.append("Education")
    if location == "Enter Location":
        missing_fields.append("Work Location")
    if job_title == "Enter Job Title":
        missing_fields.append("Job Title")

    if missing_fields:
        st.warning(f"⚠️ Please fill in the following fields before submitting: {', '.join(missing_fields)}")
    else:
        # Prepare features for prediction
        features = np.array([[
            education_encoding[education],
            experience,
            location_encoding[location],
            job_title_encoding[job_title],
            age,
            gender_encoding[gender]
        ]])
        df = pd.DataFrame(features, columns=['education_level', 'experience', 'location', 'job_title', 'age', 'gender'])

        # Predict Salary
        predicted_salary = model.predict(df)[0]

        # Color-coded salary range
        if predicted_salary < 30000:
            salary_color = "red"
            salary_msg = "Below average salary range"
        elif predicted_salary < 70000:
            salary_color = "orange"
            salary_msg = "Average salary range"
        else:
            salary_color = "green"
            salary_msg = "Above average salary range"

        st.markdown(f"### 💰 Estimated Monthly Salary: <span style='color:{salary_color};'>₹{predicted_salary:,.2f}</span>", unsafe_allow_html=True)
        st.markdown(f"**{salary_msg}**")

        # ===== City-Based Salary Adjustment =====
        st.markdown("### 🌆 Cost-of-Living Adjustment")
        target_city = st.selectbox(
            "Compare salary for relocation to:",
            list(city_multipliers.keys()),
            key="target_city"
        )
        adjusted_salary = adjust_salary_by_city(predicted_salary, current_city, target_city)
        
        # Display comparison
        col1, col2 = st.columns(2)
        with col1:
            st.metric(f"Salary in {current_city}", f"₹{predicted_salary:,.2f}")
        with col2:
            st.metric(
                f"Equivalent in {target_city}", 
                f"₹{adjusted_salary:,.2f}",
                delta=f"{((adjusted_salary - predicted_salary)/predicted_salary)*100:.1f}%"
            )

        # ===== Salary Comparison Bar Chart =====
        fig_city = px.bar(
            x=[current_city, target_city],
            y=[predicted_salary, adjusted_salary],
            labels={"x": "City", "y": "Adjusted Salary (₹)"},
            title=f"Salary Comparison: {current_city} vs {target_city}",
            color=[current_city, target_city],
            text=[f"₹{predicted_salary:,.0f}", f"₹{adjusted_salary:,.0f}"]
        )
        st.plotly_chart(fig_city, use_container_width=True)

        # ===== Salary Distribution Pie Chart =====
        st.markdown("### 📊 Salary Distribution in Industry")
        labels = ['Below Average (<₹30k)', 'Average (₹30k-₹70k)', 'Above Average (>₹70k)']
        values = [25, 50, 25]  # Example percentages
        fig_pie = px.pie(names=labels, values=values, title='How Does Your Salary Compare?')
        st.plotly_chart(fig_pie, use_container_width=True)

        # ===== Feature Importance Bar Chart =====
        st.markdown("### 🔍 What Factors Affect Your Salary?")
        feature_importance = model.feature_importances_
        features_list = ['Education', 'Experience', 'Location', 'Job Title', 'Age', 'Gender']
        fig_bar = px.bar(x=features_list, y=feature_importance, title='Feature Importance', labels={'x': 'Feature', 'y': 'Importance'})
        st.plotly_chart(fig_bar, use_container_width=True)

        # ===== Feature Correlation Heatmap =====
        st.markdown("### 🔗 How Are Features Related?")
        corr_matrix = pd.DataFrame({
            'Education': [1.0, 0.6, 0.3, 0.5],
            'Experience': [0.6, 1.0, 0.2, 0.4],
            'Location': [0.3, 0.2, 1.0, 0.1],
            'Salary': [0.5, 0.4, 0.1, 1.0]
        }, index=['Education', 'Experience', 'Location', 'Salary'])
        fig_heatmap = px.imshow(corr_matrix, text_auto=True, title='Feature Correlation')
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # ===== Radar Chart: Profile Match =====
        st.markdown("### 🎯 How Does Your Profile Compare to the Ideal?")
        categories = ['Education', 'Experience', 'Technical Skills', 'Soft Skills']
        user_values = [education_encoding[education], experience, 70, 60]  # Example user scores
        ideal_values = [4, 10, 90, 80]  # Example ideal scores
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=user_values,
            theta=categories,
            fill='toself',
            name='Your Profile'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=ideal_values,
            theta=categories,
            fill='toself',
            name='Ideal Profile'
        ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
        st.plotly_chart(fig_radar, use_container_width=True)

        # ===== What-If Scenarios =====
        st.markdown("### 🔄 What-If Scenarios")
        what_if = st.selectbox("What if...", ["I get a Master's degree", "I gain 5 more years of experience"])
        if what_if == "I get a Master's degree":
            new_features = features.copy()
            new_features[0][0] = education_encoding["Master's"]
            new_salary = model.predict(new_features)[0]
            st.write(f"🎓 New predicted salary with a Master's degree: ₹{new_salary:,.2f}")
        elif what_if == "I gain 5 more years of experience":
            new_features = features.copy()
            new_features[0][1] += 5
            new_salary = model.predict(new_features)[0]
            st.write(f"⏳ New predicted salary with 5 more years of experience: ₹{new_salary:,.2f}")

        # ===== Summary Card =====
        st.markdown("### 📝 Summary & Recommendations")
        summary = f"""
        - **Education Level:** {education}  
        - **Experience:** {experience} years  
        - **Age:** {age} years  
        - **Job Title:** {job_title}  
        - **Location:** {location}  
        - **Gender:** {gender}  
        - **Current City:** {current_city}  

        Your predicted salary is ₹{predicted_salary:,.2f} with an expected growth rate of {growth_rate}%.  
        This projection considers your current profile and market trends.
        """
        st.info(summary)

        # ===== Career Tips =====
        st.markdown("### 🎯 Career Advice & Tips")
        tips = {
            'Clerk': "📚 Learn spreadsheet tools like Excel and automation basics.<br>🧠 Improve time management and digital record handling.",
            'Customer Support': "🎧 Master CRM tools like Salesforce.<br>📞 Sharpen your empathy and conflict resolution skills.",
            'Data Analyst': "📊 Master SQL, Python, and Tableau/Power BI.<br>📈 Turn raw data into actionable business insights.",
            'Data Scientist': "🤖 Practice machine learning & deep learning.<br>📚 Participate in Kaggle, learn PyTorch & Big Data tools.",
            'Director': "🏗️ Lead with strategic thinking and vision.<br>📈 Learn stakeholder management and business transformation.",
            'HR Manager': "💼 Strengthen HR analytics and labor law knowledge.<br>🧠 Upskill in employee engagement & DEI practices.",
            'Product Manager': "🧪 Learn agile, SCRUM, and user-centric design.<br>📊 Blend business acumen with data-driven decisions.",
            'Software Engineer': "💻 Sharpen coding, DSA, and system design.<br>🌐 Master DevOps, scalable systems, and cloud tech.",
            'Technician': "🛠️ Learn diagnostics and automation tools.<br>⚙️ Certify in hardware, networking, or cloud services."
        }

        if job_title in tips:
            st.markdown(f"""
            <div style='
                background-color: #1b512cff;
                padding: 15px;
                border-radius: 10px;
                font-size: 16px;
                line-height: 1.6;
                color: white;
            '>
                {tips[job_title]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("🚀 Keep building your expertise and networking in your domain!")

# ===== Footer =====
st.markdown("""
<hr>
<div style="text-align:center">
    <strong>Think ahead. Earn smart. A Prachi Deore creation</strong><br>
    <small>Powered by Streamlit and Plotly</small>
</div>
""", unsafe_allow_html=True)
