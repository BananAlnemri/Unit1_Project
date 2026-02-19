# هذا الملف يحتوي على منطق تحليل البيانات
# ويولد تعليقات تحسين بناءً على مقارنة النتائج بالقيم المرجعية

from utils.standards import (
    sleep_target_by_age,
    water_target_liters,
    steps_target,
    self_time_target_minutes
)

# ================= Sleep Comment =================
def comment_sleep(age: int, sleep_hours: float):
    lo, hi = sleep_target_by_age(age)

    if sleep_hours is None:
        return "No sleep data available"

    if sleep_hours < lo:
        return f"Sleep below target. Aim for {lo}-{hi} hours. Try earlier bedtime and reduce screen time."

    if sleep_hours > hi:
        return f"Sleep above target. Target is {lo}-{hi} hours. Keep consistent sleep schedule."

    return f"Sleep within healthy range {lo}-{hi} hours. Keep your routine."


# ================= Water Comment =================
def comment_water(age: int, gender: str, water_liters: float):
    target = water_target_liters(age, gender)

    if water_liters is None:
        return "No water data available"

    if water_liters < target:
        return f"Water below target. Aim for {target} L daily. Spread intake through the day."

    return f"Water meets target of {target} L. Maintain consistency."


# ================= Work Study Comment =================
def comment_work(work_hours: float, sleep_hours: float, mood: float):
    if work_hours is None:
        return "No work data available"

    # ضغط عمل مع قلة نوم
    if sleep_hours is not None and work_hours >= 8 and sleep_hours < 7:
        return "High work hours with low sleep. Adjust schedule and protect sleep time."

    # إنتاجية منخفضة ومزاج منخفض
    if mood is not None and work_hours <= 2 and mood <= 3:
        return "Low work and low mood. Start with one small task tomorrow."

    return "Work balance looks stable. Continue structured planning."


# ================= Steps Comment =================
def comment_steps(age: int, steps: float):
    lo, hi = steps_target(age)

    if steps is None:
        return "No steps data available"

    if steps < lo:
        return f"Steps below target. Aim for {lo}-{hi}. Add short walks during the day."

    if steps > hi:
        return f"Steps above target {lo}-{hi}. Ensure proper recovery."

    return f"Steps within target range {lo}-{hi}. Keep it up."


# ================= Mood Comment =================
def comment_mood(mood: float, self_time_min: float):
    if mood is None:
        return "No mood data available"

    # مزاج منخفض مع وقت ذاتي قليل
    if mood <= 3:
        if self_time_min is not None and self_time_min < self_time_target_minutes():
            return "Mood low with limited self time. Add at least 15 minutes personal time."

        return "Mood low. Add light activity and short breaks."

    return "Mood stable. Keep habits that support your mental state."


# ================= Self Time Comment =================
def comment_self_time(self_time_min: float):
    target = self_time_target_minutes()

    if self_time_min is None:
        return "No hobby data available"

    if self_time_min < target:
        return f"Self time below target. Aim for at least {target} minutes daily."

    return f"Self time meets target of {target} minutes."


# ================= Full Summary =================
def full_comment(comments: list):
    # إزالة التعليقات الفارغة
    clean = [c for c in comments if c and "No" not in c]

    if not clean:
        return "Add more data to generate a full summary."

    # أخذ أهم تعليقين
    return "Summary: " + " ".join(clean[:2])
