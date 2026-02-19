import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.storage import load_days, get_day
from utils.insights import (
    comment_sleep,
    comment_water,
    comment_work,
    comment_steps,
    comment_mood,
    comment_self_time,
    full_comment
)

st.set_page_config(page_title="Result", layout="wide")

st.title("Result Page")

# زر الرجوع
if st.button("Back"):
    st.switch_page("Main.py")

# تأكد أن المستخدم اختار يوم
if "selected_date" not in st.session_state or not st.session_state.selected_date:
    st.warning("Please select a day from Main Page first")
    st.stop()

selected_date = st.session_state.selected_date
st.write(f"Selected Day: {selected_date}")

# تحميل البيانات
df = load_days()
day = get_day(df, selected_date)

if not day:
    st.warning("No data found for this day")
    st.stop()

# استخراج القيم
sleep = day["sleep_hours"]
work = day["work_hours"]
steps = day["steps"]
water = day["water"]
mood = day["mood"]
self_time = day["self_time"]

# بيانات المستخدم الافتراضية
age = 23
gender = "female"

# دالة رسم شارت بسيط
def draw_chart(title, value):
    fig, ax = plt.subplots()
    ax.bar([title], [value])
    ax.set_title(title)
    st.pyplot(fig)

# Sleep
st.subheader("Sleep")
draw_chart("Sleep Hours", sleep)
msg_sleep = comment_sleep(age, sleep)
st.write(msg_sleep)

# Water
st.subheader("Water")
draw_chart("Water Intake", water)
msg_water = comment_water(age, gender, water)
st.write(msg_water)

# Work
st.subheader("Work Hours")
draw_chart("Work Hours", work)
msg_work = comment_work(work, sleep, mood)
st.write(msg_work)

# Steps
st.subheader("Steps")
draw_chart("Steps", steps)
msg_steps = comment_steps(age, steps)
st.write(msg_steps)

# Mood
st.subheader("Mood")
draw_chart("Mood", mood)
msg_mood = comment_mood(mood, self_time)
st.write(msg_mood)

# Self Time
st.subheader("Self Time")
draw_chart("Self Time", self_time)
msg_self = comment_self_time(self_time)
st.write(msg_self)

# Summary
st.divider()
st.subheader("Full Summary")
st.write(full_comment([msg_sleep, msg_water, msg_work, msg_steps, msg_mood, msg_self]))
