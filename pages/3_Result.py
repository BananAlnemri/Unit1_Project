import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# قراءة البيانات من CSV
from utils.storage import load_days, get_day

# القيم المرجعية للأهداف
from utils.standards import (
    sleep_target_by_age,
    water_target_liters,
    steps_target,
    self_time_target_minutes,
)

# دوال التعليقات التحليلية
from utils.insights import (
    comment_sleep,
    comment_water,
    comment_work,
    comment_steps,
    comment_mood,
    comment_self_time,
    full_comment,
)

st.set_page_config(page_title="Result", layout="wide")
st.title("Result Page")

# ================= Header =================
top_left, top_right = st.columns([1, 1])

with top_left:
    st.write("Selected Day")

with top_right:
    if st.button("Back"):
        st.switch_page("Main.py")

# ================= Validate selected day =================
if "selected_date" not in st.session_state or not st.session_state.selected_date:
    st.warning("Select a day from Main Page first")
    st.stop()

selected_date = st.session_state.selected_date
st.write(selected_date)

# ================= Load day data =================
df = load_days()
day = get_day(df, selected_date)

if not day:
    st.warning("No data found for this day")
    st.stop()

# ================= User info =================
if "age" not in st.session_state:
    st.session_state.age = 23
if "gender" not in st.session_state:
    st.session_state.gender = "female"
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"

age = int(st.session_state.age)
gender = st.session_state.gender

st.write(f"Hello {st.session_state.user_name}")

# ================= Extract numeric values =================
sleep = pd.to_numeric(day.get("sleep_hours"), errors="coerce")
work = pd.to_numeric(day.get("work_hours"), errors="coerce")
steps = pd.to_numeric(day.get("steps"), errors="coerce")
water = pd.to_numeric(day.get("water"), errors="coerce")
mood = pd.to_numeric(day.get("mood"), errors="coerce")
self_time = pd.to_numeric(day.get("self_time"), errors="coerce")

# ================= Chart helpers =================
# بار بسيط لقيمة واحدة
def chart_bar_simple(title: str, label: str, value):
    fig, ax = plt.subplots()

    v = 0 if pd.isna(value) else float(value)
    ax.bar([label], [v])

    ax.set_title(title)
    st.pyplot(fig)

# بار مع خط هدف واحد
def chart_bar_with_target_line(title: str, label: str, value, target: float):
    fig, ax = plt.subplots()

    v = 0 if pd.isna(value) else float(value)
    ax.bar([label], [v])

    # خط الهدف
    ax.axhline(y=float(target), linewidth=2)

    ax.set_title(title)
    st.pyplot(fig)

# بار مع هدف على شكل مدى (min و max)
def chart_bar_with_target_band(title: str, label: str, value, target_min: float, target_max: float):
    fig, ax = plt.subplots()

    v = 0 if pd.isna(value) else float(value)
    ax.bar([label], [v])

    # خط الحد الأدنى
    ax.axhline(y=float(target_min), linewidth=2)

    # خط الحد الأعلى
    ax.axhline(y=float(target_max), linewidth=2)

    ax.set_title(title)
    st.pyplot(fig)

# ================= Card helper =================
# كرت واحد فيه شارت يسار وتعليق يمين
def card(title: str, chart_fn, comment_text: str):
    left, right = st.columns([2, 1])

    with left:
        st.subheader(title)
        chart_fn()

    with right:
        st.write(comment_text)

# ================= Build targets =================
sleep_min, sleep_max = sleep_target_by_age(age)
steps_min, steps_max = steps_target(age)
water_target = water_target_liters(age, gender)
self_target = self_time_target_minutes()

# ================= Grid layout =================
# صف 1: Sleep | Water
row1_left, row1_right = st.columns(2)

with row1_left:
    msg_sleep = comment_sleep(age, None if pd.isna(sleep) else float(sleep))

    def sleep_chart():
        # الهدف مدى حسب العمر
        chart_bar_with_target_band(
            title="Sleep hours",
            label="sleep",
            value=sleep,
            target_min=sleep_min,
            target_max=sleep_max,
        )

    card("Sleep", sleep_chart, msg_sleep)

with row1_right:
    msg_water = comment_water(age, gender, None if pd.isna(water) else float(water))

    def water_chart():
        # الهدف رقم واحد حسب العمر والجنس
        chart_bar_with_target_line(
            title="Water liters",
            label="water",
            value=water,
            target=water_target,
        )

    card("Water", water_chart, msg_water)

# صف 2: Work | Steps
row2_left, row2_right = st.columns(2)

with row2_left:
    msg_work = comment_work(
        None if pd.isna(work) else float(work),
        None if pd.isna(sleep) else float(sleep),
        None if pd.isna(mood) else float(mood),
    )

    def work_chart():
        # ما عندنا معيار ثابت للعمل
        chart_bar_simple(
            title="Work hours",
            label="work",
            value=work,
        )

    card("Study or Work", work_chart, msg_work)

with row2_right:
    msg_steps = comment_steps(age, None if pd.isna(steps) else float(steps))

    def steps_chart():
        # الهدف مدى حسب العمر
        chart_bar_with_target_band(
            title="Steps",
            label="steps",
            value=steps,
            target_min=steps_min,
            target_max=steps_max,
        )

    card("Steps", steps_chart, msg_steps)

# صف 3: Mood | Self time
row3_left, row3_right = st.columns(2)

with row3_left:
    msg_mood = comment_mood(
        None if pd.isna(mood) else float(mood),
        None if pd.isna(self_time) else float(self_time),
    )

    def mood_chart():
        # المزاج مقياس صغير 1 إلى 5
        chart_bar_simple(
            title="Mood score",
            label="mood",
            value=mood,
        )

    card("Mood", mood_chart, msg_mood)

with row3_right:
    msg_self = comment_self_time(None if pd.isna(self_time) else float(self_time))

    def self_chart():
        # الهدف رقم واحد ثابت
        chart_bar_with_target_line(
            title="Self time minutes",
            label="self time",
            value=self_time,
            target=self_target,
        )

    card("Self time", self_chart, msg_self)

# ================= Full summary =================
st.divider()
st.subheader("Full comment for all result")
st.write(full_comment([msg_sleep, msg_water, msg_work, msg_steps, msg_mood, msg_self]))
