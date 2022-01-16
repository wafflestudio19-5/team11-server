from .models import Lecture
from django.db.models import Q

def filter_lectures(lectures, query):
    if 'subject_name' in query:
        subject_name = query.get('subject_name')
        if subject_name:
            q = Q()
            keywords = set(subject_name.split(' '))
            for k in keywords:
                q &= Q(subject_professor__subject_name__icontains=k)
            lectures = lectures.filter(q)
        else:
            lectures = Lecture.objects.none()

    if 'subject_code' in query:
        subject_code = query.get('subject_code')
        if subject_code:
            lectures = lectures.filter(subject_code__icontains=subject_code)
        else:
            lectures = Lecture.objects.none()

    if 'professor' in query:
        professor = query.get('professor')
        if professor:
            lectures = lectures.filter(subject_professor__professor__icontains=professor)
        else:
            lectures = Lecture.objects.none()

    if 'year' in query:
        try:
            year = int(query.get('year'))
            lectures = lectures.filter(year=year)
        except Exception:
            lectures = Lecture.objects.none()

    if 'season' in query:
        try:
            season = int(query.get('season'))
            lectures = lectures.filter(season=season)
        except Exception:
            lectures = Lecture.objects.none()

    if 'department' in query:
        query_department = query.get('department').split(' ')
        if len(query_department) == 1:
            college = query_department[0]
            lectures = lectures.filter(college=college)
        elif len(query_department) == 2:
            college, department = query_department
            lectures = lectures.filter(college=college, department=department)

    if 'grade' in query:
        try:
            grade = [int(i) for i in query.get('grade').split(' ')]
            lectures = lectures.filter(grade__in=grade)
        except Exception:
            lectures = Lecture.objects.none()

    if 'level' in query:
        try:
            level = [int(i) for i in query.get('level').split(' ')]
            lectures = lectures.filter(level__in=level)
        except Exception:
            lectures = Lecture.objects.none()

    if 'credit' in query:
        try:
            credit = [int(i) for i in query.get('credit').split(' ')]
            lectures = lectures.filter(credit__in=credit)
        except Exception:
            lectures = Lecture.objects.none()

    if 'category' in query:
        try:
            category = [int(i) for i in query.get('category').split(' ')]
            lectures = lectures.filter(category__in=category)
        except Exception:
            lectures = Lecture.objects.none()

    if 'language' in query:
        language = query.get('language').split(' ')
        lectures = lectures.filter(language__in=language)

    if 'location' in query:
        location = query.get('location')
        if location:
            lectures = lectures.filter(location__icontains=location)
        else:
            lectures = Lecture.objects.none()

    return lectures