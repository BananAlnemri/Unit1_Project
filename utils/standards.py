# هذا الملف يحتوي على القيم المرجعية التي نقارن بها بيانات المستخدم

# ================= Sleep Target =================
# إرجاع الحد الأدنى والأعلى لساعات النوم حسب العمر
def sleep_target_by_age(age: int):
    if age <= 3:
        return (10, 13)
    if age <= 5:
        return (10, 13)
    if age <= 12:
        return (9, 12)
    if age <= 17:
        return (8, 10)
    if age <= 64:
        return (7, 9)
    return (7, 8)


# ================= Water Target =================
# إرجاع كمية الماء الموصى بها باللتر حسب العمر والجنس
def water_target_liters(age: int, gender: str):
    g = (gender or "").strip().lower()

    if age <= 3:
        return 1.0
    if age <= 8:
        return 1.2
    if age <= 13:
        if g in ["male", "m", "boy", "ذكر"]:
            return 1.6
        return 1.4
    if age <= 18:
        if g in ["male", "m", "boy", "ذكر"]:
            return 1.9
        return 1.6

    # للبالغين
    if g in ["male", "m", "man", "men", "ذكر"]:
        return 2.6
    return 2.1


# ================= Steps Target =================
# إرجاع الحد الأدنى والأعلى للخطوات حسب العمر
def steps_target(age: int):
    if age >= 60:
        return (6000, 8000)
    return (8000, 10000)


# ================= Self Time Target =================
# إرجاع الحد الأدنى الموصى به لوقت الهوايات أو الوقت الشخصي بالدقائق
def self_time_target_minutes():
    return 15
