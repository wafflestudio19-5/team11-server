from .models import Lecture
from django.db.models import Q

def filter_lectures(lectures, query):
    if 'subject' in query:
        subject = query.get('subject')
        if not subject:
            lectures = Lecture.objects.none()
        else:
            q = Q()
            keywords = set(subject.split(' '))
            for k in keywords:
                q &= Q(subject_professor__subject_name__icontains=k)
            lectures = lectures.filter(q)

    if 'subject_code' in query:
        subject_code = query.get('subject_code')
        if not subject_code:
            lectures = Lecture.objects.none()
        else:
            lectures = lectures.filter(subject_code=subject_code)

    if 'professor' in query:
        professor = query.get('professor')
        if not professor:
            lectures = Lecture.objects.none()
        else:
            lectures = lectures.filter(subject_professor__professor__icontains=professor)

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
        department = query.get('department').split(' ')
        lectures = lectures.filter(department__in=department)

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
        locations = query.get('location').split(' ')
        if not locations:
            lectures = Lecture.objects.none()
        else:
            q = Q()
            for k in locations:
                q &= Q(location__icontains=k + "-")
            lectures = lectures.filter(q)

    return lectures