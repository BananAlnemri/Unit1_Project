import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

from utils.storage import load_days
from utils.insights import (
    comment_sleep,
    comment_water,
    comment_work,
    comment_steps,
    comment_mood,
    comment_self_time,
    full_comment
)

st.set_page_config(page_title="Weekly Report", layout="wide")

st.title("Weekly Report")

# زر رجوع
if st.button("Back"):
    st.switch_page("Main.py")

# بيانات المستخدم الافتراضية
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"
if "age" not in st.session_state:
    st.session_state.age = 23
if "gender" not in st.session_state:
    st.session_state.gender = "female"

age = int(st.session_state.age)
gender = st.session_state.gender

st.write(f"Hello {st.session_state.user_name}")

# تحميل البيانات من CSV
df = load_days()

if df.empty:
    st.info("No days added yet")
    st.stop()

# فلترة آخر 7 أيام
today = date.today()
start_day = today - timedelta(days=6)

df_valid = df.dropna(subset=["date"]).copy()
df_week = df_valid[(df_valid["date"] >= start_day) & (df_valid["date"] <= today)].copy()

if df_week.empty:
    st.info("No records in the last 7 days")
    st.stop()

# تحويل الأعمدة إلى أرقام
for col in ["sleep_hours", "work_hours", "steps", "water", "mood", "self_time"]:
    df_week[col] = pd.to_numeric(df_week[col], errors="coerce")

# حساب المتوسطات
avg_sleep = float(df_week["sleep_hours"].mean())
avg_work = float(df_week["work_hours"].mean())
avg_steps = float(df_week["steps"].mean())
avg_water = float(df_week["water"].mean())
avg_mood = float(df_week["mood"].mean())
avg_self = float(df_week["self_time"].mean())

st.subheader("Weekly averages (last 7 days)")
c1, c2, c3 = st.columns(3)
c1.metric("Sleep hours", f"{avg_sleep:.1f}")
c2.metric("Work hours", f"{avg_work:.1f}")
c3.metric("Steps", f"{avg_steps:.0f}")

c4, c5, c6 = st.columns(3)
c4.metric("Water (L)", f"{avg_water:.1f}")
c5.metric("Mood", f"{avg_mood:.1f}")
c6.metric("Self time (min)", f"{avg_self:.0f}")

st.divider()

# رسم خطي بسيط لكل مؤشر عبر الأسبوع
def line_chart(title: str, series: pd.Series):
    fig, ax = plt.subplots()
    ax.plot(df_week["date"], series)
    ax.set_title(title)
    ax.set_xlabel("Date")
    st.pyplot(fig)

c7, c8 = st.columns(2)

with c7:
    st.subheader("Sleep chart")
    line_chart("Sleep hours", df_week["sleep_hours"])
    msg_sleep = comment_sleep(age, avg_sleep)
    st.write(msg_sleep)

with c8:
    st.subheader("Drink water chart")
    line_chart("Water liters", df_week["water"])
    msg_water = comment_water(age, gender, avg_water)
    st.write(msg_water)

c9, c10 = st.columns(2)

with c9:
    st.subheader("Study/work hour chart")
    line_chart("Work hours", df_week["work_hours"])
    msg_work = comment_work(avg_work, avg_sleep, avg_mood)
    st.write(msg_work)

with c10:
    st.subheader("Steps chart")
    line_chart("Steps", df_week["steps"])
    msg_steps = comment_steps(age, avg_steps)
    st.write(msg_steps)

c11, c12 = st.columns(2)

with c11:
    st.subheader("Mood chart")
    line_chart("Mood", df_week["mood"])
    msg_mood = comment_mood(avg_mood, avg_self)
    st.write(msg_mood)

with c12:
    st.subheader("Hobby chart")
    line_chart("Self time minutes", df_week["self_time"])
    msg_self = comment_self_time(avg_self)
    st.write(msg_self)

st.divider()

st.subheader("Full comment for weekly result")
st.write(full_comment([msg_sleep, msg_water, msg_work, msg_steps, msg_mood, msg_self]))
