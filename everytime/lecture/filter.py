from .models import Lecture, SubjectProfessor
from django.db.models import Q

def filter_subject_professor(subject_professors, query):

    if 'subject_name' in query:
        subject_name = query.get('subject_name')
        if subject_name:
            q = Q()
            keywords = set(subject_name.split(' '))
            for k in keywords:
                q &= Q(subject_name__icontains=k)
            subject_professors = subject_professors.filter(q)
        else:
            subject_professors = SubjectProfessor.objects.none()

    if 'professor' in query:
        professor = query.get('professor')
        if professor:
            subject_professors = subject_professors.filter(professor__icontains=professor)
        else:
            subject_professors = SubjectProfessor.objects.none()

    return subject_professors

def filter_lectures(lectures, query):
    if 'sort' in query:
        criteria = query.get('sort')
        if criteria == 'subject_code':
            lectures = lectures.order_by('subject_code')
        elif criteria  == 'subject_name':
            lectures = lectures.order_by('subject_professor__subject_name')

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
            lectures = lectures.filter(college__name=college)
        elif len(query_department) == 2:
            college, department = query_department
            lectures = lectures.filter(college__name=college, department__name=department)
        elif len(query_department) > 2:
            college = query_department[0]
            department = ' '.join(query_department[1:])
            lectures = lectures.filter(college__name=college, department__name=department)

    if 'grade' in query:
        try:
            grade = [int(i) for i in query.get('grade').split(' ')]
            if 5 in grade:
                temp = lectures.exclude(grade__in=[1,2,3,4])
                grade.remove(5)
                temps = lectures.filter(grade__in=grade)
                lectures = temp | temps
            else:
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
            if 4 in credit:
                temp = lectures.filter(credit__gt=3)
                credit.remove(4)
                temps = lectures.filter(credit__in=credit)
                lectures = temp | temps
            else:
                lectures = lectures.filter(credit__in=credit)
        except Exception:
            lectures = Lecture.objects.none()

    if 'category' in query:
        try:
            category = [Lecture.CategoryCode[i] for i in query.get('category').split(' ')]
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