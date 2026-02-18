# teacher/utils.py
from datetime import date
from core.models import Lecture, daily_lecturres

def generate_today_lectures(teacher):
    today = date.today()
    day = today.strftime('%A')

    timetable_entries = Lecture.objects.filter(
        teacher=teacher,
        day=day
    )

    for entry in timetable_entries:
        daily_lecturres.objects.get_or_create(
            teacher=entry.teacher,
            batch=entry.batch,
            subject=entry.subject,
            class_date=today,
            weekday=day,
            start_time=entry.start_time,
             defaults={
                'weekday': day,
                'end_time': entry.end_time,
                'created_from_timetable': entry
            }
        )
