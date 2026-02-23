#Leen,Ibtihal
#Library :
import streamlit as st #for streamlit
from datetime import date, datetime #for allwoing to work with calenar dates directly 
import plotly.graph_objects as go #for low level,object oriented interface fot=r creating figures 
from abc import ABC, abstractmethod   # needed for OOP Abstraction
# ─────────────────────────────────────────────────────────────
#Raghad
# Database setup: Save user data 

import json  # used to convert Python data to JSON file
from pathlib import Path  # used to safely handle file paths

DB_PATH = Path("database.json") # This file will store users and their entries

# ─────────────────────────────────────────────────────────────
# Load Database
# Reads data from database.json
# If file does not exist, create one

def load_db() : # This function return a dictionary

    if not DB_PATH.exists(): # Check if database file exists

        # Create file with default structure
        default_data = {
            "users": [],     # list of registered users
            "entries": {}    # dictionary: user_email : list of daily entries
        }
        # Creat empty json file in the first run
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2) # Note: "dump" converts Python structure → JSON text
        
        return default_data
    
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db): # Save Database and writes updated data into database.json
    with open(DB_PATH, "w", encoding="utf-8") as f: # Overwrites old data with updated data
        # Convert Python dictionary to JSON format
        json.dump(
            db, f,
            ensure_ascii=False,  # allow normal text
            indent=2             # make the file readable
        )

# Load database once when app starts
# This keeps db available during app runtime

db = load_db()
# ─────────────────────────────────────────────────────────────
# Page Config : setting up specific parameters,layout,metadata for web pag/app interface 
#Leen 
st.set_page_config( # Streamlit setup basic page settings for the app

    page_title="Habby",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ─────────────────────────────────────────────────────────────
# Session State : to share vairbales between renruns , for each uesr session 
#Leen 
#Raghad 
def init_session() : #function creates default values for the session,So every user starts with clean data

    defaults = {
        "page":       "home",   # str  > current page
        "user":       None,     # dict > stores logged-in user info
        "entries":    [],       # list > list of daily log entries
        "edit_index": None,     # int  > index of entry being edited

        # RAGHAD added
        "result_index": 0,      # int > used for browsing results without selectbox
    }
    #It iterates through each element in the dictionary, checks if the variable already exists, and places it in session_state.
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()


# ─────────────────────────────────────────────────────────────
# Lambda function : the basic quick functions to use on login page 
#Leen 
#Banan
validate_email    = lambda email: "@" in email and "." in email.split("@")[-1] #user must use @ when they enter their email
validate_password = lambda pwd:   len(pwd) >= 6 #the password must be more than 6 characters
get_avg           = lambda lst:   sum(lst) / len(lst) if lst else 0.0 #get_avg calculates average safely (returns 0 if list is empty)


# ─────────────────────────────────────────────────────────────
# Helper Function : Basic functions for comparing user data with official studies to extract results on the results page 
#Leen
#Basic information about human sleep needs based on age
def get_sleep_recommendation(age: int) :
    if age <= 5:
        return {"min": 10, "max": 14, "label": "Young child"}
    elif age <= 12:
        return {"min": 9,  "max": 13, "label": "Child"}
    elif age <= 17:
        return {"min": 8,  "max": 10, "label": "Teen"}
    elif age <= 64:
        return {"min": 7,  "max": 9,  "label": "Adult"}
    else:
        return {"min": 7,  "max": 8,  "label": "Senior"}

#Basic information about human needs for drinling water based on age
def get_water_recommendation(age: int, gender: str) :
#(1 L ≈ 4 cups)
    g = gender.lower() #The gender is converted to lowercase for comparison.
    if age <= 3:
        liters: float = 1.0
    elif age <= 8:
        liters = 1.2
    elif age <= 13:
        liters = 1.6 if g == "male" else 1.4
    elif age <= 18:
        liters = 1.9 if g == "male" else 1.6
    else:
        liters = 2.6 if g == "male" else 2.1
    return round(liters * 4, 1)

#Basic information about human steps needs based on age
def get_steps_recommendation(age: int) :
    if age <= 17:
        return 12_000
    elif age >= 60:
        return 7_000
    else:
        return 10_000

#The advice the user will receive based on the results of the information entered and a comparison between approved basic information.
def generate_comment(metric: str, value: float, user: dict) : #enter (habit name ,avg , user info) 
    #How finction works :
    #This function generates a personalised comment
      #1- take the age and user gender :
    age = user["age"]
    gender = user["gender"]
    comment: str = ""
      #2- see which matric is :
    if metric == "sleep":
      #3- get the recommendation ( we alrady made )
        rec: dict = get_sleep_recommendation(age)
      #4- compare 
        if value < rec["min"]:
      #5- bulid the comments (comment is varible we'll call it letter) :
            comment = (
                "You have been sleeping a little less than your body needs."
                f"For your age {rec['min']}–{rec['max']} hours is a healthy range."
                "Rest is not a luxury. It is part of how you take care of yourself."
            )
        elif value > rec["max"]:
            comment = (
                "You have been sleeping more than your body usually requires."
                f"For your age {rec['min']}–{rec['max']} hours is generally enough."
                "A regular routine can help you feel lighter through the day."
            )
        else:
            comment = (
                "Your sleep is in a healthy place."
                f"For your age {rec['min']}–{rec['max']} hours supports balance and clarity."
                "There is something beautiful about keeping a steady rhythm."
            )

    elif metric == "water":
        rec_cups: float = get_water_recommendation(age, gender)
        if value < rec_cups:
            comment = (
                "Your water intake is a little below what your body needs."
                f"For you {rec_cups} cup per day is a healthy guide."
                 "Staying hydrated is a quiet way of caring for your energy and focus."
            )
        else:
            comment = (
                "You are meeting your daily water needs."
                "This level of hydration supports balance and clarity."
                "Small steady habits like this shape how you feel."
            )

    elif metric == "steps":
        rec_steps: int = get_steps_recommendation(age)
        if value < rec_steps:
            comment = (
                "Your movement has been lighter than recommended."
                f"For your age {rec_steps:,} steps is a healthy range."
                "Even simple daily movement can gently lift your energy."
                )
        else:
            comment = (
                "You are reaching your movement goal."
                "Regular activity supports both physical strength and emotional balance."
                "There is strength in steady effort."
            )

    elif metric == "mood":
        if value <= 4:
            comment = (
                "Your mood has been on the lower side."
                "Rest routine and small positive moments can help restore balance."
                "Give yourself patience. Not every season feels the same."
            )
        elif value <= 7:
            comment = (
                "Your mood feels steady."
                "Simple habits like sleep movement and hydration help keep this balance."
                "There is quiet strength in stability."
            )
        else:
            comment = (
                "Your mood has been strong."
                "Protect the habits and connections that support this feeling."
                "Joy grows where it is gently cared for."
            )

    elif metric == "study":
        if value < 2:
            comment = (
                "Your focused time has been limited."
                "Even one protected hour each day can shift your momentum."
                "Consistency matters more than intensity."
            )
        elif value > 10:
            comment = (
                "You have been working long hours."
                "Make space for recovery so your energy can renew."
                "Sustainable progress is always stronger than burnout."
            )
        else:
            comment = (
                "Your work rhythm looks healthy."
                "Balancing effort with rest allows you to sustain your performance."
                "There is wisdom in pacing yourself."
            )

    elif metric == "hobby":
        if value < 0.5:
            comment = (
                "There has been little time just for you."
                "Even a short period of something you enjoy can soften the weight of the day."
                "Joy deserves space in your routine."
            )
        else:
            comment = (
                "You are giving time to hobbies."
                "Creative and restful moments support emotional balance."
                "This kind of care strengthens you quietly."
            )

    return comment

# summary for the result page ; getting from stady user infon
def generate_overall_summary(entries: list, user: dict) :
    if not entries: #guard clause : if the list empty return nothing 
        return ""
    #info extraction 
    age= user["age"]
    gender= user["gender"]
    #calculating the avg : 
    avg_sleep: float = get_avg([e["sleep"] for e in entries]) #List Comprehension : take [sleep] value from each entry and claculate the avg
    avg_water: float = get_avg([e["water"] for e in entries])
    avg_steps: float = get_avg([e["steps"] for e in entries])
    avg_mood:  float = get_avg([e["mood"]  for e in entries])
    avg_study: float = get_avg([e["study"] for e in entries])
    avg_hobby: float = get_avg([e["hobby"] for e in entries])
    #bring the recommendation 
    sleep_rec = get_sleep_recommendation(age)
    water_rec = get_water_recommendation(age, gender)
    steps_rec = get_steps_recommendation(age)

    positives= [] #positive things
    issues   = [] #things need improve 

    if sleep_rec["min"] <= avg_sleep <= sleep_rec["max"]: #Chained Comparison
        positives.append("Sleep")
    else:
        issues.append("Sleep")

    if avg_water >= water_rec:
        positives.append("Hydration")
    else:
        issues.append("Hydration")

    if avg_steps >= steps_rec:
        positives.append("Steps")
    else:
        issues.append("Steps")

    if avg_mood >= 7:
        positives.append("Mood")
    else:
        issues.append("Mood")

    if 2 <= avg_study <= 10:
        positives.append("Study / Work")
    else:
        issues.append("Study / Work")

    if avg_hobby >= 0.5:
        positives.append("Hobbies")
    else:
        issues.append("Hobbies")

    lines: list = []
    if positives:
        lines.append(f"Doing well in: {', '.join(positives)}.") #join : converted the list to comma-separated text
    if issues:
        lines.append(f"Areas to improve: {', '.join(issues)}.")

    lines.append(
        "Small steady habits shape how you feel over time. "
        "Sleep well, stay hydrated, move gently, and let consistency do the work."
    )

    if len(issues) == 0:
        lines.append("You are in a strong and balanced place. Keep caring for what is already working.")
    elif len(issues) <= 2:
        lines.append(
            "You are moving in the right direction. "
            "A little attention to these areas will gently strengthen the whole picture."
        )
    else:
        lines.append(
            "Pick one area to focus on this week. "
            "Small steady changes create real progress."
        )

    return "\n\n".join(lines)


# ─────────────────────────────────────────────────────────────
# Chart : Graphs chart to display the results of user data analysis and study
#Leen
#colors palet : 
PASTEL_COLORS = [
    "#E8A87C",  # peach
    "#A0B89A",  # sage green
    "#89B4CC",  # sky blue
    "#E8A0A8",  # blush pink
    "#C5B4E3",  # lavender
    "#D4B483",  # warm gold
]


def hex_to_rgba(hex_color: str, alpha: float = 0.12) -> str:
    hex_color = hex_color.lstrip("#") #delete (#) from the start
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4)) # conv from hexa to decimal
    return f"rgba({r},{g},{b},{alpha})" #return in way plotly can undrstand it 


def make_chart(dates: list, values: list, color: str, unit: str):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode="lines+markers",
        line=dict(color=color, width=2.5, shape="spline", smoothing=0.6),
        marker=dict(size=8, color=color, line=dict(color="#EDE8DF", width=2)),
        fill="tozeroy",
        fillcolor=hex_to_rgba(color, alpha=0.12),
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#5a5550", family="DM Sans", size=11),
        xaxis=dict(
            type="category",  # هذا السطر يضمن ظهور التواريخ كفئات وليس ساعات
            gridcolor="#D9D4CB",
            showgrid=True,
            tickfont=dict(color="#8a8277", size=10),
            tickangle=-45,    # ميلان التاريخ ليكون أوضح إذا كثرت الأيام
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor="#D9D4CB",
            showgrid=True,
            title=unit,
            tickfont=dict(color="#8a8277", size=10),
            zeroline=False,
        ),
        margin=dict(l=0, r=0, t=10, b=40), # زيادة الهامش السفلي للتاريخ
        height=250, # زيادة الارتفاع قليلاً لتنسيق أفضل
    )
    return fig
# ─────────────────────────────────────────────────────────────
# RAGHAD added
# Sorting helper so browsing works stable :

def sort_entries_by_date(entries: list) -> list:
    def to_dt(e: dict) -> datetime:
        try:
            return datetime.strptime(e.get("date", ""), "%Y-%m-%d")
        except Exception:
            return datetime.min
    return sorted(entries, key=to_dt)

# ─────────────────────────────────────────────────────────────
# RAGHAD added
# Render chart + comment side by side : 

def render_metric_side_by_side(title: str, fig: go.Figure, comment_text: str) -> None:
    st.markdown(f'<p class="label-sm">{title}</p>', unsafe_allow_html=True)

    col_chart, col_text = st.columns([1.2, 1.0])
    with col_chart:
        st.plotly_chart(fig, width="stretch")
    with col_text:
        st.markdown(
            f'<div class="comment-block" style="margin-top:0">{comment_text}</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────
# OOP section : 
#leen 

# ─────────────────────────────────────────────────────────────
#ENCAPSULATION 
#leen
class User:
    

    def __init__(self, name: str, email: str, password: str,
                 age: int, gender: str) : #The User class stores all user data in private attributes
        self.__name       = name        
        self.__email      = email
        self.__password   = password
        self.__age        = age
        self.__gender     = gender
        self.__registered = True        

    # Read-only properties :
    @property
    def name(self)       : return self.__name

    @property
    def age(self)        :  return self.__age

    @property
    def gender(self)     :  return self.__gender

    @property
    def registered(self) : return self.__registered

    def to_dict(self) :
        return {
            "name":       self.__name,
            "email":      self.__email,
            "password":   self.__password,
            "age":        self.__age,
            "gender":     self.__gender,
            "registered": self.__registered,
        }

    @staticmethod
    def from_dict(data) :
        return User(
            name     = data["name"],
            email    = data["email"],
            password = data["password"],
            age      = data["age"],
            gender   = data["gender"],
        )

# ─────────────────────────────────────────────────────────────
#ABSTRACTION
#Leen
# HealthMetric acts as a contract 
class HealthMetric(ABC):
    

    def __init__(self, value: float, user: User) :
        self._value = value  
        self._user  = user    # original user dict, unchanged

    @property
    def value(self) :
        return self._value
    
# Return the healthy target for this metric
    @abstractmethod
    def recommendation(self) :
        
        pass

# Return personalised feedback for the current value
    @abstractmethod
    def comment(self) :
        
        pass

# ─────────────────────────────────────────────────────────────
# INHERITANCE + POLYMORPHISM : 
#leen
# Each class below inherits from HealthMetric and gives its own
# version of recommendation() and comment().

class SleepMetric(HealthMetric): #Sleep rules depend on age only."""
    

    def recommendation(self) :
        return get_sleep_recommendation(self._user.age)   # reuse original function

    def comment(self) :
        return generate_comment("sleep", self._value, self._user)   # reuse original function


class WaterMetric(HealthMetric): #Water rules depend on age AND gender
    

    def recommendation(self) :
        cups = get_water_recommendation(self._user.age, self._user.gender)
        return {"cups": cups}

    def comment(self) :
        return generate_comment("water", self._value, self._user)


class StepsMetric(HealthMetric): #Steps target drops for older adults.
    

    def recommendation(self) :
        return {"steps": get_steps_recommendation(self._user.age)}

    def comment(self) :
        return generate_comment("steps", self._value, self._user)


class MoodMetric(HealthMetric): #Mood is a 1–10 score, no age/gender dependency.
    

    def recommendation(self) :
        return {"min": 7, "max": 10}

    def comment(self) :
        return generate_comment("mood", self._value, self._user)


class StudyMetric(HealthMetric): #Study has a low threshold (under-working) and a high threshold (burnout).
    

    def recommendation(self) :
        return {"min": 2, "max": 10}

    def comment(self) :
        return generate_comment("study", self._value, self._user)


class HobbyMetric(HealthMetric): #Even 30 min/day of hobbies counts as healthy.
    

    def recommendation(self) :
        return {"min": 0.5}

    def comment(self) :
        return generate_comment("hobby", self._value, self._user)

#─────────────────────────────────────────────────────────────
#Factory function (uses Polymorphism) 
#leen
#Returns the correct HealthMetric subcl ass for a given key.
def build_metric(key: str, avg_value: float, user: User) :
    
    classes = {
        "sleep": SleepMetric,
        "water": WaterMetric,
        "steps": StepsMetric,
        "mood":  MoodMetric,
        "study": StudyMetric,
        "hobby": HobbyMetric,
    }
    return classes[key](avg_value, user)




# ─────────────────────────────────────────────────────────────
# Global style :
#leen

def apply_styles() :
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif !important;
    }
    .stApp {
        background-color: #EDE8DF;
        min-height: 100vh;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── Layout ── */
    .block-container {
        max-width: 520px !important;
        padding: 2.5rem 1.4rem 5rem !important;
        margin: 0 auto;
    }

    /* ── Typography ── */
    .display-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.75rem;
        color: #1a1a1a;
        text-align: center;
        letter-spacing: -0.4px;
        line-height: 1.15;
        margin-bottom: 0.3rem;
    }
    .page-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.9rem;
        color: #1a1a1a;
        letter-spacing: -0.3px;
        margin-bottom: 0.2rem;
        margin-top: 0;
    }
    .body-muted {
        color: #8a8277;
        font-size: 0.9rem;
        font-weight: 400;
        line-height: 1.55;
        margin: 0;
    }
    .label-sm {
        font-size: 0.72rem;
        font-weight: 600;
        color: #8a8277;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.6rem;
        margin-top: 0;
    }

    /* ── Dividers ── */
    .thin-rule {
        border: none;
        border-top: 1px solid #D9D4CB;
        margin: 1.6rem 0;
    }

    /* ── Color strip ── */
    .color-strip {
        display: flex;
        gap: 5px;
        margin: 1.2rem 0 0.4rem;
        height: 5px;
    }
    .strip-seg {
        flex: 1;
        border-radius: 6px;
    }

    /* ── Pills ── */
    .pill {
        display: inline-block;
        border-radius: 30px;
        padding: 0.28rem 0.8rem;
        font-size: 0.76rem;
        font-weight: 500;
        margin: 0.18rem 0.12rem;
        font-family: 'DM Sans', sans-serif;
    }
    .pill-yellow { background: #F5E49A; color: #6b5c00; }
    .pill-green  { background: #BFD9B7; color: #2a6124; }
    .pill-blue   { background: #B8D4E8; color: #1c4c70; }
    .pill-pink   { background: #EEC8CC; color: #7a2838; }
    .pill-sage   { background: #CEDFBF; color: #34572c; }
    .pill-peach  { background: #F2D1B8; color: #7a3d18; }
                
    .features-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        max-width: 320px;
        margin: 20px auto 0 auto;
        justify-items: center;
    }

    /* ── Entry rows (dashboard) ── */
    .entry-row {
        padding: 1rem 0;
        border-bottom: 1px solid #D9D4CB;
    }
    .entry-date-label {
        font-family: 'DM Serif Display', serif;
        font-size: 1rem;
        color: #1a1a1a;
        margin-bottom: 0.45rem;
    }

    /* ── Form inputs ── */
    .stTextInput input,
    .stNumberInput input {
        background: #F5F1EA !important;
        border: 1px solid #1a1a1a !important;
        border-radius: 10px !important;
        color: #1a1a1a !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.91rem !important;
        padding: 0.55rem 0.9rem !important;
        box-shadow: none !important;
    }
                
    /* Placeholder text color */
    .stTextInput input::placeholder {
        color: #8a8277 !important;   
        opacity: 1 !important;      
    }

    .stNumberInput input::placeholder {
        color: #8a8277 !important;
        opacity: 1 !important;
    }
    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: #A0B89A !important;
        box-shadow: 0 0 0 3px rgba(160,184,154,0.2) !important;
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background: #F5F1EA !important;
        border: 1px solid #D9D4CB !important;
        border-radius: 10px !important;
        color: #1a1a1a !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Slider ── */
    .stSlider [data-baseweb="thumb"] {
        background: #A0B89A !important;
        border-color: #A0B89A !important;
    }
    .stSlider [data-baseweb="track-fill"] {
        background: #A0B89A !important;
    }

    /* ── Form labels ── */
    label,
    .stSlider label,
    .stNumberInput label,
    .stTextInput label,
    .stSelectbox label {
        color: #5a5550 !important;
        font-weight: 500 !important;
        font-size: 0.87rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Buttons ── */
    div[data-testid="stButton"] > button {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        border-radius: 50px !important;
        padding: 0.55rem 1.5rem !important;
        transition: all 0.18s ease !important;
        letter-spacing: 0.1px !important;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: #1a1a1a !important;
        color: #EDE8DF !important;
        border: none !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: #2e2e2e !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"] {
        background: transparent !important;
        color: #5a5550 !important;
        border: 1px solid #C8C3BA !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"]:hover {
        background: #E5E0D7 !important;
    }

    /* ── Error / info alerts ── */
    div[data-testid="stAlert"] {
        background: #4a4a47 !important;
        border: 1px solid #D9D4CB !important;
        border-left: 3px solid #89B4CC !important;
        border-radius: 0 10px 10px 0 !important;
        color: #1a1a1a !important;
        font-size: 0.87rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Comment block ── */
    .comment-block {
        background: #F5F1EA;
        border-left: 3px solid #A0B89A;
        border-radius: 0 10px 10px 0;
        padding: 0.85rem 1rem;
        font-size: 0.86rem;
        color: #3a3630;
        line-height: 1.65;
        margin-top: 0.4rem;
        font-family: 'DM Sans', sans-serif;
    }
                /* تعديل لون نص خيارات الجنس ليصبح أسود وواضح */
        div[data-testid="stRadio"] label p {
            color: #262730 !important;
            font-weight: 500 !important;
        }
                
    </style>
    """, unsafe_allow_html=True)



#PAGES : 

# ─────────────────────────────────────────────────────────────
# PAGE 1 — "HOME" :
#Leen #Edited by Banan%Ibtihal%Raghad
def page_home() : #fun draw home page 
    st.markdown('<div class="display-title">Habby</div>', unsafe_allow_html=True)#display HTML inside Streamlit
    # Short description under title
    st.markdown(
        '<p class="body-muted" style="text-align:center;margin-bottom:0.5rem">'
        "Tiny habits. Big change.</p>", 
        unsafe_allow_html=True,
    )

    # Decorative colour strip (just for design)
    st.markdown(
        '<div class="color-strip">'
        '<div class="strip-seg" style="background:#F5D97A"></div>'
        '<div class="strip-seg" style="background:#A0B89A"></div>'
        '<div class="strip-seg" style="background:#89B4CC"></div>'
        '<div class="strip-seg" style="background:#E8A0A8"></div>'
        '<div class="strip-seg" style="background:#E8A87C"></div>'
        "</div>",
        unsafe_allow_html=True,
    )
    # Small horizontal line
    st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
    
#will be display in the interface in circles containing the names
    features = [
        ("Steps",     "pill-green"),
        ("Hydration", "pill-blue"),
        ("Sleep",     "pill-yellow"),
        ("Mood",      "pill-pink"),
        ("Hobbies",   "pill-sage"),
        ("Study",     "pill-peach"),
    ]
    # RAGHAD fix
    # build all pills in ONE HTML block so they actually stay inside the container
    pills_html = ""
    for name, cls in features:
        pills_html += f'<div class="pill {cls}">{name}</div>'

    st.markdown(
        f'<div class="features-container">{pills_html}</div>',
        unsafe_allow_html=True
    )

    # Space before button
    st.markdown('<div style="margin-top:40px;"></div>', unsafe_allow_html=True)

    # Get Started button
    if st.button("Get started", use_container_width=True, type="primary"):
        st.session_state.page = "register"
        st.rerun()

    # Login button to go to login page
    if st.button("Log in", use_container_width=True):
        st.session_state.page = "login"
        st.rerun()
# ─────────────────────────────────────────────────────────────
# PAGE 2 — REGISTER : 
# Banan #Edited by Banan%Ibtihal

def page_register() :
    #Back button
    if st.button("Back", type="secondary"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="page-title">Create account</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="body-muted" style="margin-bottom:1.6rem">'
        "A few details, and we’ll tailor the experience for you</p>",
        unsafe_allow_html=True,
    )

# ───────────── INPUTS ─────────────
    user_name = st.text_input(
        "Full Name",
        placeholder="Enter your full name"
    )
    user_email = st.text_input(
        "Email",
        placeholder="example@email.com"
    )
    user_password = st.text_input(
        "Password",
        type="password",
        placeholder="At least 6 characters"
    )
    user_age = st.number_input(
        "Age",
        min_value=18,
        max_value=120,
        step=1
    )
    # Gender selection (ONLY Male / Female)
    user_gender = st.radio(
        "Select Gender",
        options=["Female", "Male"]
    )
    st.markdown("<br>", unsafe_allow_html=True)


    # ───────────── CREATE BUTTON ─────────────

    if st.button("Create Account", use_container_width=True):

        error_list = []

        # Validate name
        if user_name.strip() == "":
            error_list.append("Name cannot be empty.")

        # Validate email
        if "@" not in user_email or "." not in user_email:
            error_list.append("Enter a valid email.")

        # Validate password
        if len(user_password) < 6:
            error_list.append("Password must be at least 6 characters.")

        # Show errors
        if error_list:
            for error in error_list:
                st.error(error)

        
        # If everything is valid
        else:
# ─────────────────────────────────────────────────────────────
# Raghad Edited this

            # ───────── Save to database.json first ─────────
            db = load_db()

            # Check if email already exists
            for u in db["users"]:
                if u["email"] == user_email:
                    st.error("This email is already registered. Please log in.")
                    st.stop()

            new_user = {
                "name": user_name.strip(),

                "email": user_email,

                "password": user_password,

                "age": int(user_age),

                "gender": user_gender,

                "registered": True
            }

            # save to db
            db["users"].append(new_user)
            
            # create empty entries list for this user
            if user_email not in db["entries"]:
                db["entries"][user_email] = []

            save_db(db)

            # Save user in session state
            st.session_state.user = new_user

            # Initialize entries list
            st.session_state.entries = []

            # Go to dashboard
            st.session_state.page = "dashboard"

            st.success("Account created successfully!")

            st.rerun()
# ─────────────────────────────────────────────────────────────
# PAGE 3 — LOGIN :
# Raghad

def page_login():

    # Back button returns user to home page
    if st.button("Back", type="secondary"):
        st.session_state.page = "home"
        st.rerun()

    # Small spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Page title
    st.markdown('<div class="page-title">Log in</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="body-muted" style="margin-bottom:1.6rem">'
        "Enter your email and password.</p>",
        unsafe_allow_html=True,
    )

    
    # ───────────── INPUT FIELDS ─────────────

    # User enters email
    login_email = st.text_input(
        "Email",
        placeholder="example@email.com"
    )

    # User enters password (hidden)
    login_password = st.text_input(
        "Password",
        type="password",
        placeholder="Your password"
    )

    # ───────────── LOGIN BUTTON ─────────────

    if st.button("Log in", use_container_width=True, type="primary"):

        # Load database from JSON file
        db = load_db()

        # Variable to store matched user
        found_user = None

        # Loop through all registered users
        for u in db["users"]:

            # Check if both email and password match
            if u["email"] == login_email and u["password"] == login_password:
                found_user = u
                break

        # If no matching user found → show error
        if found_user is None:
            st.error("Email or password is incorrect.")
            return

        # If match found → store full user dict in session
        st.session_state.user = found_user

        # Load this specific user's saved entries from database
        # If no entries exist yet → return empty list
        st.session_state.entries = db["entries"].get(login_email, [])

        # Reset browsing index for results pages
        st.session_state.result_index = 0

        # Redirect to dashboard
        st.session_state.page = "dashboard"

        st.success("Welcome back!")
        st.rerun()
# ─────────────────────────────────────────────────────────────
# PAGE 4 — DASHBOARD :
#Ibtihal , leen edited 

def page_dashboard() : #Displays the dashboard page

    user = st.session_state.user #Get user data
    entries = st.session_state.entries #Get all saved daily entries
    today = date.today().strftime("%B %d, %Y") #Display today's date in format

    #Greeting message with user's name
    st.markdown(
        f'<div class="page-title">Hello, {user["name"]}.</div>',
        unsafe_allow_html=True,
    )
    #Display today's date
    st.markdown(
        f'<p class="body-muted">{today}</p>',
          unsafe_allow_html=True
          )
    #Divider line
    st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
    
    #Checks if there are no days entered
    if not entries:
        st.markdown('<p class="label-sm">Logged days</p>', unsafe_allow_html=True)
    else:
    #ُThe list of color for each metric pill

        pill_cycle: list = [
            "pill-yellow", "pill-green", "pill-blue",
            "pill-pink",   "pill-sage",  "pill-peach",
        ]
        #Define each one and its display
        metric_labels: list = [
            ("sleep", "h sleep"),
            ("water", " cups"),
            ("steps", " steps"),
            ("mood",  "/10 mood"),
            ("study", "h study"),
            ("hobby", "h hobby"),
        ]

        for i, entry in enumerate(entries): #Newest day first
            pills_html = ""
            for (key, suffix), cls in zip(metric_labels, pill_cycle):
                val: float = entry[key]
                display: str = f"{int(val):,}" if key == "steps" else f"{val}"
                pills_html += f'<span class="pill {cls}">{display}{suffix}</span>'
            
            st.markdown(
                f'<div class="entry-row">'
                f'<div class="entry-date-label">{entry["date"]}</div>'
                f"<div>{pills_html}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )
            
            #Edit button per entry 
            if st.button(f"Edit  {entry['date']}", key=f"edit_btn_{i}", type="secondary"):
                st.session_state.edit_index = i
                st.session_state.page       = "add_day"
                st.rerun()

    st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    #Navigate to add day page
    if c1.button("Add day", use_container_width=True, type="primary"):
        st.session_state.edit_index = None
        st.session_state.page = "add_day"
        st.rerun()

    #Navigate to track page (disabled if no entries)
    if c2.button(" Show Track", use_container_width=True, disabled=(len(entries) == 0)):
        st.session_state.page = "track"
        st.rerun()
# ─────────────────────────────────────────────────────────────
# PAGE 5 — ADD / EDIT DAY
#  #Leen, Edited by Banan+Ibtihal


def page_add_day():
    edit_index = st.session_state.get("edit_index")
    is_edit = edit_index is not None
    entries = st.session_state.entries

    # الإعدادات الافتراضية مع إضافة مفتاح التاريخ
    defaults = {
        "date":  date.today(),
        "sleep": 7.0,
        "study": 1.0,
        "steps": 5000.0,
        "water": 1.0,
        "mood":  7,
        "hobby": 1.0,
    }

    # إذا كنا في وضع التعديل، نسحب التاريخ القديم ونحوله لصيغة يفهمها التقويم
    if is_edit and edit_index < len(entries):
        old = entries[edit_index]
        if "date" in old:
            try:
                defaults["date"] = datetime.strptime(old["date"], "%Y-%m-%d").date()
            except:
                defaults["date"] = date.today()
        
        # تحديث باقي القيم
        for k in ["sleep", "study", "steps", "water", "mood", "hobby"]:
            defaults[k] = old.get(k, defaults[k])

    if st.button("Back", type="secondary"):
        st.session_state.edit_index = None
        st.session_state.page       = "dashboard"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    heading: str = "Edit entry" if is_edit else "Add day"
    st.markdown(f'<div class="page-title">{heading}</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="body-muted" style="margin-bottom:1.6rem">'
        "Log your habits and build your progress</p>",
        unsafe_allow_html=True,
    )

    # 1. مدخل التاريخ
# 1. مدخل التاريخ مع تحديد الحد الأقصى بتاريخ اليوم
    user_selected_date = st.date_input(
        "Select Date",
        value=defaults["date"],
        max_value=date.today()  # هذا السطر يمنع اختيار أي تاريخ في المستقبل
    )
    selected_str: str = user_selected_date.strftime("%Y-%m-%d")

    date_to_index: dict = {e["date"]: i for i, e in enumerate(entries)}

    # A duplicate exists when the chosen date is already saved
    # AND we are NOT currently editing that same entry
    existing_index = date_to_index.get(selected_str)
    is_duplicate   = (
        existing_index is not None and
        not (is_edit and edit_index == existing_index)
    )

    if is_duplicate:
        # Show the old saved data so the user can see what they logged
        existing = entries[existing_index]
        st.warning(f"You already have an entry for **{selected_str}**. Your saved data is shown below.")

        pill_cycle = ["pill-yellow","pill-green","pill-blue","pill-pink","pill-sage","pill-peach"]
        labels     = [
            ("sleep","h sleep"),("water"," cups"),("steps"," steps"),
            ("mood","/10 mood"),("study","h study"),("hobby","h hobby"),
        ]
        pills_html = ""
        for (key, suffix), cls in zip(labels, pill_cycle):
            val = existing.get(key, 0)
            display = f"{int(val):,}" if key == "steps" else f"{val}"
            pills_html += f'<span class="pill {cls}">{display}{suffix}</span>'
        st.markdown(f'<div style="margin:0.8rem 0">{pills_html}</div>', unsafe_allow_html=True)

        # Button to open that existing entry for editing
        if st.button(f"Edit entry for {selected_str}", use_container_width=True, type="primary"):
            st.session_state.edit_index = existing_index
            st.session_state.page       = "add_day"
            st.rerun()

        return   

    # 2. بقية المدخلات الرقمية
    sleep_hours: float = st.number_input(
        "Sleep hours",
        min_value=0.0, max_value=24.0,
        value=float(defaults["sleep"]), step=0.5,
    )
    study_hours: float = st.number_input(
        "Study / work hours",
        min_value=0.0, max_value=24.0,
        value=float(defaults["study"]), step=0.5,
    )
    steps: float = st.number_input(
        "Steps walked",
        min_value=0.0, max_value=100_000.0,
        value=float(defaults["steps"]), step=100.0,
    )
    water_cups: float = st.number_input(
        "Water cups",
        min_value=0.0, max_value=30.0,
        value=float(defaults["water"]), step=0.5,
    )
    
    # 3. ساعات الهوايات
    hobby_hours: float = st.number_input(
        "Hobby hours",
        min_value=0.0, max_value=24.0,
        value=float(defaults["hobby"]), step=0.5,
    )

    # 4. التعديل: السكيل حق المود أصبح هنا (آخر مدخل)
    mood: int = st.slider(
        "How do you feel Today?",
        min_value=1, max_value=10,
        value=int(defaults["mood"]),
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Save", use_container_width=True, type="primary"):
        new_entry: dict = {
            "date":  user_selected_date.strftime("%Y-%m-%d"),
            "sleep": sleep_hours,
            "study": study_hours,
            "steps": steps,
            "water": water_cups,
            "mood":  mood,
            "hobby": hobby_hours,
        }
        
        if is_edit:
            entries[edit_index] = new_entry
        else:
            entries.append(new_entry)

        st.session_state.entries    = entries
        # ─────────────────────────────────────────
        # Save entries permanently to database.json
        # Raghad

        db = load_db()

        # Current logged in user email (used as key)
        current_email = st.session_state.user["email"]

        # Make sure user has an entries list in db
        if current_email not in db["entries"]:
            db["entries"][current_email] = []

        # Save updated entries list for this user
        db["entries"][current_email] = st.session_state.entries

        # Write changes to file
        save_db(db)
        # ─────────────────────────────────────────
        st.session_state.edit_index = None
        st.session_state.page       = "dashboard"
        st.rerun()


# ─────────────────────────────────────────────────────────────
# PAGE 6 — TRACK (result page) :
#Leen #Edited by Banan%Ibtihal
def page_track():
    user = st.session_state.user
    entries_raw = st.session_state.entries

    if st.button("Back", type="secondary"):
        st.session_state.page = "dashboard"
        st.rerun()

    

    if not entries_raw:
        st.info("No data to display. Add a day first.")
        return

    # التعديل: ترتيب البيانات زمنياً قبل استخراج المحاور لضمان دقة الرسم
    entries = sort_entries_by_date(entries_raw)
    
    dates: list = [e["date"] for e in entries] 
    

    # Each tuple: (metric_key, label, values, colour, y-axis unit)
    metrics: list = [
        ("sleep", "Sleep hours",        [e["sleep"] for e in entries], PASTEL_COLORS[1], "Hours"),
        ("water", "Water cups",         [e["water"] for e in entries], PASTEL_COLORS[2], "Cups"),
        ("study", "Study / work hours", [e["study"] for e in entries], PASTEL_COLORS[0], "Hours"),
        ("steps", "Steps walked",       [e["steps"] for e in entries], PASTEL_COLORS[4], "Steps"),
        ("mood",  "Mood score",         [e["mood"]  for e in entries], PASTEL_COLORS[3], "Score"),
        ("hobby", "Hobby hours",        [e["hobby"] for e in entries], PASTEL_COLORS[5], "Hours"),
    ]

    for metric, title, vals, color, unit in metrics:
        avg_val: float = get_avg(vals)
        st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
        st.markdown(f'<p class="label-sm">{title}</p>', unsafe_allow_html=True)

        # width='stretch' is the current Streamlit API (use_container_width deprecated)
        st.plotly_chart(make_chart(dates, vals, color, unit), width="stretch")

        comment_text: str = generate_comment(metric, avg_val, user)
        st.markdown(
            f'<div class="comment-block">{comment_text}</div>',
            unsafe_allow_html=True,
        )

    # Overall summary
    st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
    st.markdown('<p class="label-sm">Overall summary</p>', unsafe_allow_html=True)
    summary: str = generate_overall_summary(entries, user)
    st.markdown(
        f'<div class="comment-block" style="border-left-color:#89B4CC">{summary}</div>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Back to dashboard", use_container_width=True, type="primary"):
        st.session_state.page = "dashboard"
        st.rerun()

# ─────────────────────────────────────────────────────────────
# RAGHAD added
# PAGE 7 — TODAY RESULTS
# Browsing without selectbox
# Chart + text side by side

def page_results_today() -> None:
    user: dict = st.session_state.user
    entries_raw: list = st.session_state.entries

    if st.button("Back", type="secondary"):
        st.session_state.page = "dashboard"
        st.rerun()
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="page-title">Today results</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="body-muted" style="margin-bottom:0.5rem">'
        "Browse days with Next and Previous.</p>",
        unsafe_allow_html=True,
    )

    if not entries_raw:
        st.info("No data to display. Add a day first.")
        return

    entries: list = sort_entries_by_date(entries_raw)

    # RAGHAD added
    # keep index inside range
    if st.session_state.result_index < 0:
        st.session_state.result_index = 0
    if st.session_state.result_index > len(entries) - 1:
        st.session_state.result_index = len(entries) - 1

    nav_prev, nav_mid, nav_next = st.columns([1, 1.3, 1])
    with nav_prev:
        if st.button("Previous", use_container_width=True, disabled=(st.session_state.result_index == 0)):
            st.session_state.result_index -= 1
            st.rerun()
    with nav_mid:
        st.markdown(
            f'<p class="label-sm" style="text-align:center;margin-top:0.6rem">'
            f'{entries[st.session_state.result_index]["date"]}'
            f"</p>",
            unsafe_allow_html=True,
        )
    with nav_next:
        if st.button("Next", use_container_width=True, disabled=(st.session_state.result_index == len(entries) - 1)):
            st.session_state.result_index += 1
            st.rerun()

    st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)

    e: dict = entries[st.session_state.result_index]

    # RAGHAD added
    # single point chart using bar so it fits as a daily result
    metrics: list = [
        ("sleep", "Sleep", e["sleep"], PASTEL_COLORS[1], "Hours"),
        ("water", "Water", e["water"], PASTEL_COLORS[2], "Cups"),
        ("study", "Study", e["study"], PASTEL_COLORS[0], "Hours"),
        ("steps", "Steps", e["steps"], PASTEL_COLORS[4], "Steps"),
        ("mood",  "Mood",  e["mood"],  PASTEL_COLORS[3], "Score"),
        ("hobby", "Hobby", e["hobby"], PASTEL_COLORS[5], "Hours"),
    ]

    for metric_key, label, value, color, unit in metrics:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[label],
            y=[value],
            marker_color=color,
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#5a5550", family="DM Sans", size=11),
            margin=dict(l=0, r=0, t=10, b=0),
            height=220,
            yaxis=dict(title=unit, gridcolor="#D9D4CB", zeroline=False),
            xaxis=dict(gridcolor="#D9D4CB", zeroline=False),
        )

        comment_text: str = generate_comment(metric_key, float(value), user)

        st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
        render_metric_side_by_side(label, fig, comment_text)

    st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
    st.markdown('<p class="label-sm">Overall</p>', unsafe_allow_html=True)

    overall_text: str = generate_overall_summary([e], user)
    st.markdown(
        f'<div class="comment-block" style="border-left-color:#89B4CC">{overall_text}</div>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# RAGHAD added
# PAGE 8 — WEEKLY RESULTS       #Edited by Banan%Ibtihal
# last 7 entries line charts + comment beside chart

def page_results_week() -> None:
    user: dict = st.session_state.user
    entries_raw: list = st.session_state.entries

    if st.button("Back", type="secondary"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="page-title">Weekly results</div>', unsafe_allow_html=True)
    st.markdown(
        '<p class="body-muted" style="margin-bottom:0.5rem">'
        "Shows the latest 7 logged days.</p>",
        unsafe_allow_html=True,
    )

    if not entries_raw:
        st.info("No data to display. Add a day first.")
        return

    entries_sorted: list = sort_entries_by_date(entries_raw)
    week_entries: list = entries_sorted[-7:]

    dates: list = [e["date"] for e in week_entries]

    metrics: list = [
        ("sleep", "Sleep", [e["sleep"] for e in week_entries], PASTEL_COLORS[1], "Hours"),
        ("water", "Water", [e["water"] for e in week_entries], PASTEL_COLORS[2], "Cups"),
        ("study", "Study", [e["study"] for e in week_entries], PASTEL_COLORS[0], "Hours"),
        ("steps", "Steps", [e["steps"] for e in week_entries], PASTEL_COLORS[4], "Steps"),
        ("mood",  "Mood",  [e["mood"]  for e in week_entries], PASTEL_COLORS[3], "Score"),
        ("hobby", "Hobby", [e["hobby"] for e in week_entries], PASTEL_COLORS[5], "Hours"),
    ]

    for metric_key, label, vals, color, unit in metrics:
        avg_val: float = get_avg(vals)
        fig: go.Figure = make_chart(dates, vals, color, unit)
        comment_text: str = generate_comment(metric_key, avg_val, user)

        st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
        render_metric_side_by_side(label, fig, comment_text)

    st.markdown('<hr class="thin-rule">', unsafe_allow_html=True)
    st.markdown('<p class="label-sm">Overall summary</p>', unsafe_allow_html=True)

    summary: str = generate_overall_summary(week_entries, user)
    st.markdown(
        f'<div class="comment-block" style="border-left-color:#89B4CC">{summary}</div>',
        unsafe_allow_html=True,
    )
    
# ─────────────────────────────────────────────────────────────
# Router :
# Edited by Raghad
apply_styles()

_page: str        = st.session_state.page
_protected: tuple = ("dashboard", "add_day", "track")

# Redirect to home if user tries to access a protected page without logging in
if _page in _protected and st.session_state.user is None:
    st.session_state.page = "home"
    st.rerun()

if   _page == "home":      page_home()
elif _page == "register":  page_register()
elif _page == "login":     page_login()
elif _page == "dashboard": page_dashboard()
elif _page == "add_day":   page_add_day()
elif _page == "track":     page_track()
else:
    st.session_state.page = "home"
    st.rerun()
