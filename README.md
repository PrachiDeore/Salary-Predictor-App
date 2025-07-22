## Employee Salary Predictor App💼💰
An interactive web application built with Streamlit that predicts employee salaries based on profiles, adjusts for cost-of-living across cities, and provides career insights.

🔗 Live Demo: 

## ✨ Key Features
- ✅ Salary Prediction – Estimates earnings using education, experience, job title, and more.
- 🌆 City-Based Adjustments – Compares salaries across cities (e.g., ₹12L in Pune ≈ ₹16.8L in Mumbai).
- 📊 Visualizations – Interactive charts for salary distribution, feature importance, and relocation planning.
- 🎯 Career Advice – Tailored tips for job titles (e.g., Data Scientist, HR Manager).
- 🔄 What-If Scenarios – Explore impact of higher education or experience.

## 📂 Project Structure
```
Employee-Salary-Predictor-Pro/
│
├── salary_predictor_enhanced.py  # Main Streamlit app (with city adjustments)
├── rf_model_compressed.pkl      # Pre-trained Random Forest model
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```
## ⚙️ Installation & Setup
1. Clone the repository:
```
git clone https://github.com/yourusername/Employee-Salary-Predictor-Pro.git
cd Employee-Salary-Predictor-Pro
```
2. Set up a virtual environment:
```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```
3. Install dependencies:
```
pip install -r requirements.txt
```
Launch the app:
```
streamlit run app.py
```
## 📋 Input Parameters
```
Education Level: High School, Bachelor's, Master's, PhD
Years of Experience: 0–30
Age: 18–65
Gender: Male/Female
Job Title: Clerk, Data Scientist, HR Manager, etc.
Location: Urban/Rural
City	Mumbai, Bangalore, Pune, etc.
```
## 🛠️ How It Works
- Enter candidate details in the form.
- Predict to generate salary and city-adjusted equivalents.
- Compare salaries across cities for relocation planning.
- Explore career tips and what-if scenarios.

## 📜 License
This project is licensed under the [MIT License](LICENSE).
