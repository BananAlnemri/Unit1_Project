import streamlit as st
import pandas as pd
from datetime import date
from utils.storage import load_days, save_days

st.set_page_config(page_title="Add Day", layout="wide")

st.title("Add Day")

# عرض تاريخ اليوم
today = date.today()
st.write(f"Date: {today}")

# ================= Inputs =================

sleep = st.number_input("Sleep hours", min_value=0.0, max_value=24.0)
work = st.number_input("Work / Study hours", min_value=0.0, max_value=24.0)
steps = st.number_input("Steps", min_value=0)
water = st.number_input("Water intake (liters)", min_value=0.0)
mood = st.slider("Mood", 1, 5)
self_time = st.number_input("Self time (minutes)", min_value=0)

# ================= Save Button =================

if st.button("Add"):
    df = load_days()

    new_row = {
        "date": today,
        "sleep_hours": sleep,
        "work_hours": work,
        "steps": steps,
        "water": water,
        "mood": mood,
        "self_time": self_time,
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_days(df)

    st.success("Day added successfully")

    # الرجوع للصفحة الرئيسية
    st.switch_page("Main.py")

# زر رجوع يدوي
if st.button("Back"):
    st.switch_page("Main.py")
