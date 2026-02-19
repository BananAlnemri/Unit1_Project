import streamlit as st
from datetime import date
from utils.storage import load_days  # دالة تحميل الأيام من ملف CSV

# إعداد الصفحة
st.set_page_config(page_title="Main Page", layout="wide")

# التأكد من وجود اسم المستخدم في الجلسة
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"

# متغير لحفظ اليوم المختار
if "selected_date" not in st.session_state:
    st.session_state.selected_date = None

# عنوان الصفحة
st.title("Main Page")

# عرض تاريخ اليوم
st.write(date.today().strftime("%Y-%m-%d"))

# عرض رسالة ترحيب
st.write(f"Hello {st.session_state.user_name}")

# تحميل بيانات الأيام من الملف
days_df = load_days()

# ================== Sidebar ==================
with st.sidebar:
    st.subheader("Recorded Days")

    # إذا لا يوجد بيانات
    if days_df.empty:
        st.info("No days added yet")

    else:
        # ترتيب الأيام من الأحدث إلى الأقدم
        days_sorted = days_df.dropna(subset=["date"]).sort_values("date", ascending=False)

        # تحويل التاريخ إلى نص
        options = [d.strftime("%Y-%m-%d") for d in days_sorted["date"].tolist()]

        # اختيار يوم من القائمة
        picked = st.radio("Select a day", options, index=0)

        # زر لفتح صفحة النتيجة
        if st.button("Open result"):
            st.session_state.selected_date = picked  # حفظ اليوم المختار
            st.switch_page("pages/3_Result.py")  # الانتقال لصفحة النتائج

# ================== Main Buttons ==================

c1, c2 = st.columns(2)

# زر إضافة يوم جديد
with c1:
    if st.button("Add day"):
        st.switch_page("pages/2_Add_day.py")

# زر عرض التقرير الأسبوعي
with c2:
    if st.button("Show track"):
        st.switch_page("pages/4_Weekly_Report.py")

