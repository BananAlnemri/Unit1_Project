import os
import pandas as pd

# مسار ملف التخزين
DATA_PATH = "data/days.csv"

# الأعمدة الأساسية في ملف البيانات
COLUMNS = [
    "date",
    "sleep_hours",
    "work_hours",
    "steps",
    "water",
    "mood",
    "self_time",
]

# إنشاء ملف CSV إذا لم يكن موجود
def ensure_data_file():
    # إنشاء مجلد data إذا لم يكن موجود
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    # إذا لم يكن ملف CSV موجود يتم إنشاؤه بالأعمدة المحددة
    if not os.path.exists(DATA_PATH):
        pd.DataFrame(columns=COLUMNS).to_csv(DATA_PATH, index=False)

# تحميل جميع الأيام من ملف CSV
def load_days() -> pd.DataFrame:
    # التأكد من وجود الملف
    ensure_data_file()

    # قراءة الملف إلى DataFrame
    df = pd.read_csv(DATA_PATH)

    # تحويل عمود التاريخ إلى نوع تاريخ
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date

    return df

# حفظ البيانات في ملف CSV
def save_days(df: pd.DataFrame) -> None:
    ensure_data_file()

    # نسخ البيانات لتجنب تعديل الأصل
    out = df.copy()

    # تحويل التاريخ إلى صيغة نص قبل الحفظ
    if "date" in out.columns:
        out["date"] = pd.to_datetime(out["date"], errors="coerce").dt.strftime("%Y-%m-%d")

    # حفظ البيانات في الملف
    out.to_csv(DATA_PATH, index=False)

# جلب بيانات يوم معين باستخدام التاريخ
def get_day(df: pd.DataFrame, day_str: str):
    # إذا البيانات فارغة أو لا يوجد عمود تاريخ
    if df.empty or "date" not in df.columns:
        return None

    # تحويل التاريخ النصي إلى تاريخ
    d = pd.to_datetime(day_str, errors="coerce").date()

    # البحث عن اليوم المطابق
    match = df[df["date"] == d]

    # إذا لم يتم العثور على اليوم
    if match.empty:
        return None

    # إرجاع بيانات اليوم كقاموس
    return match.iloc[0].to_dict()
