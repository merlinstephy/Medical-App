import pandas as pd
import streamlit as st

# Load medicine dataset
try:
    df = pd.read_excel("medicinedataset.xlsx")
except FileNotFoundError:
    st.error("❌ Excel file not found! Place 'medicine_data.xlsx' in the same folder.")
    st.stop()

st.set_page_config(page_title="Medicine Risk Detector", page_icon="💊", layout="centered")
st.title("💊 Medicine Information & Risk Detection System")
st.markdown("Enter medicine, age, and allergy info to detect risks.")

# Sidebar Inputs
st.sidebar.header("User Inputs")
medicine_name = st.sidebar.selectbox("Select Medicine", df['Medicine_Name'])
user_age = st.sidebar.number_input("Enter your Age", min_value=0, max_value=120, value=25)
user_allergy = st.sidebar.text_input("Known Allergy (or None)", value="None")
combo_input = st.sidebar.text_input("Check Combination (comma separated)")

# ------------------ Functions ------------------
def age_category(age):
    if age < 12:
        return "child"
    elif age < 60:
        return "adult"
    else:
        return "senior"

def single_medicine_risk(med_name, age, allergy):
    med = df[df['Medicine_Name'].str.lower() == med_name.lower()]
    if med.empty:
        return "❌ Medicine not found."

    info = med.iloc[0]
    risk_messages = []
    
    # Allergy check
    if allergy.lower() != "none" and allergy.lower() in str(info['Allergy_Warning']).lower():
        risk_messages.append("🚫 Allergy Risk Detected!")
    
    # Age check
    age_risk_text = str(info['Age_Risk']).lower()
    user_group = age_category(age)
    if ("avoid" in age_risk_text or "caution" in age_risk_text):
        if ("children" in age_risk_text and user_group=="child") or ("infant" in age_risk_text and user_group=="child") or ("elderly" in age_risk_text and user_group=="senior"):
            risk_messages.append("⚠️ Age-based Risk Detected")
    
    # Risk level check
    if str(info['Risk_Level']).lower() == "high":
        risk_messages.append("⚠️ High Risk: Consult a doctor.")

    if not risk_messages:
        risk_messages.append("✅ No major risks detected.")
    
    return info, risk_messages

def combination_risk(meds):
    meds_list = [m.strip().lower() for m in meds.split(",") if m.strip()]
    found = df[df['Medicine_Name'].str.lower().isin(meds_list)]
    if len(found) < 2:
        return "⚠️ Enter at least 2 valid medicines for combination check."

    messages = []
    for i in range(len(found)):
        for j in range(i+1, len(found)):
            s1 = str(found.iloc[i]['Side_Effects']).lower()
            s2 = str(found.iloc[j]['Side_Effects']).lower()
            common = set(s1.split(", ")) & set(s2.split(", "))
            if common:
                messages.append(f"⚠️ {found.iloc[i]['Medicine_Name']} & {found.iloc[j]['Medicine_Name']} share side effects: {', '.join(common)}")
    if not messages:
        messages.append("✅ No overlapping side effects detected.")
    return messages

# ------------------ Display Single Medicine Info ------------------
st.subheader("Single Medicine Info & Risk")
info, risks = single_medicine_risk(medicine_name, user_age, user_allergy)
st.markdown(f"**Medicine:** {info['Medicine_Name']}")
st.markdown(f"**Use:** {info['Use']}")
st.markdown(f"**Dosage:** {info['Dosage']}")
st.markdown(f"**Side Effects:** {info['Side_Effects']}")
st.markdown(f"**Allergy Warning:** {info['Allergy_Warning']}")
st.markdown(f"**Risk Level:** {info['Risk_Level']}")
st.markdown(f"**Age Safety:** {info['Age_Risk']}")

st.markdown("**Risk Analysis:**")
for r in risks:
    st.warning(r) if "⚠️" in r or "🚫" in r else st.success(r)

# ------------------ Combination Risk ------------------
if combo_input:
    st.subheader("Combination Risk Check")
    combo_results = combination_risk(combo_input)
    for c in combo_results:
        st.warning(c) if "⚠️" in c else st.success(c)
