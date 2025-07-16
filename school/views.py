from collections import defaultdict, namedtuple
from datetime import date
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.urls import reverse


from school.forms import AdmitMemberForm, ChangePasswordForm, LoginForm
from school.models import UserBase

# Create your views here.
def home(request):
    return render(request, 'school/index.html')

def about(request):
    return render(request, 'school/about.html')

def programs(request):
    return render(request, 'school/program.html')

def contact(request):
    return render(request, 'school/contact.html')



def admit_new_member_view(request):
    if request.method == 'POST':
        form = AdmitMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Member admitted successfully.")
            return redirect('/admin/school/userbase/')
    else:
        form = AdmitMemberForm()
    return render(request, 'school/admit_member.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            password = form.cleaned_data['password']

            try:
                user = UserBase.objects.get(user_id=user_id)
                if check_password(password, user.password):
                    request.session['user_id'] = user.user_id
                    request.session['user_type'] = user.user_type

                    # 🔐 Check if first time login
                    if user.is_first_login:
                        return redirect('change_password_on_first_login')

                    # Normal redirect
                    if user.user_type == 'student':
                        return redirect('student_dashboard')
                    elif user.user_type == 'teacher':
                        return redirect('teacher_dashboard')
                    elif user.user_type == 'school':
                        return redirect('school_dashboard')
                else:
                    messages.error(request, '❌ Invalid password.')
            except UserBase.DoesNotExist:
                messages.error(request, '❌ Invalid User ID.')
    else:
        form = LoginForm()
    
    return render(request, 'school/login.html', {'form': form})


def change_password_on_first_login(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = UserBase.objects.get(user_id=user_id)

        # ⛔ Block access if not first login
        if not user.is_first_login:
            return redirect('login')  # ya student_dashboard etc.

        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.is_first_login = False
                user.save()
                messages.success(request, "✅ Password changed successfully. Now login again.")
                return redirect('login')
        else:
            form = ChangePasswordForm()

        return render(request, 'school/change_password_first.html', {'form': form})
    
    except UserBase.DoesNotExist:
        return redirect('login')
    
# ------------------------------- Student Dashboard Views ------------------------------------------
def student_dashboard(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'student':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    return render(request, 'school/student/student_dashboard.html')

def student_profile(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'student':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    print(request.path)
    return render(request, 'school/student/profile.html')

def student_examination(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'student':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    print(request.path)
    return render(request, 'school/student/examination.html')

def student_fees(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'student':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    print(request.path)
    return render(request, 'school/student/fees.html')

def student_attendence(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'student':
        return redirect('login')

    print("Session:", request.session.get('user_id'))
    print(request.path)

    attendance_data = {
        "January":   ['P', 'A', 'P', 'P', 'P', 'A', 'P'] + ['-'] * 24,
        "February":  ['P', 'P', 'A', 'P', 'A'] + ['-'] * 26,
        "March":     ['P', 'P', 'P', 'A'] + ['-'] * 27,
        "April":     ['A', 'A', 'P', 'P', 'P', 'P'] + ['-'] * 25,
        "May":       ['P'] * 20 + ['A'] * 5 + ['-'] * 6,
        "June":      ['P', 'A'] * 10 + ['-'] * 11,
    }
    date_range = range(1, 32) 
    return render(request, 'school/student/attendence.html',{
        'attendance_data': attendance_data,
        'date_range': date_range
    })

def student_study_material(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'student':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    print(request.path)
    return render(request, 'school/student/study_material.html')

def student_settings(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'student':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    print(request.path)
    return render(request, 'school/student/settings.html')


# ------------------------------- Student Dashboard Views Ends ------------------------------------------


# ------------------------------- Teacher Dashboard Views Ends ------------------------------------------

def teacher_dashboard(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'teacher':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    return render(request, 'school/teacher/teacher_dashboard.html')

def teacher_profile(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'teacher':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    print(request.path)
    return render(request, 'school/teacher/profile.html')

def teacher_attendance(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'teacher':
        return redirect('login')

    attendance_data = {
        "January": ['P', 'A', 'P', 'L', 'P'] + ['-'] * 26,
        "February": ['P'] * 15 + ['L'] * 2 + ['A'] * 1 + ['-'] * 10,
        "March": ['P'] * 20 + ['A'] * 1 + ['-'] * 10,
        "April": ['P', 'L', 'P'] * 5 + ['-'] * 16,
        "May": ['P'] * 18 + ['A'] * 2 + ['-'] * 11,
        "June": ['L'] * 3 + ['P'] * 20 + ['-'] * 7,
    }
    date_range = range(1, 32)

    return render(request, 'school/teacher/attendance.html', {
        'attendance_data': attendance_data,
        'date_range': date_range
    })


def assigned_courses(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'teacher':
        return redirect('login')  # Or use your login URL name

    # Replace with actual model/query
    # Sample dummy data
    raw_courses = [
        {'classes': '12th', 'section': 'A', 'subject_name': 'Maths', 'subject_code': 'MATH301', 'session': '2024-2025'},
        {'classes': '12th', 'section': 'A', 'subject_name': 'Physics', 'subject_code': 'PHY302', 'session': '2024-2025'},
        {'classes': '11th', 'section': 'B', 'subject_name': 'Chemistry', 'subject_code': 'CHE201', 'session': '2024-2025'},
        {'classes': '11th', 'section': 'B', 'subject_name': 'Biology', 'subject_code': 'BIO202', 'session': '2024-2025'},
    ]

    # Grouping logic
    grouped = defaultdict(list)
    GroupKey = namedtuple('GroupKey', ['classes', 'section', 'session'])

    for course in raw_courses:
        key = GroupKey(course['classes'], course['section'], course['session'])
        grouped[key].append(course)

    return render(request, 'school/teacher/courses.html', {
        'grouped_courses': dict(grouped)
    })


def teacher_evaluation(request):
    # Dummy class-wise student data
    class_data = {
        '12A': [
            {'id': 'STD25001', 'name': 'Ayush Patel'},
            {'id': 'STD25002', 'name': 'Rekha Singh'},
            {'id': 'STD25003', 'name': 'Riya Sharma'},
            {'id': 'STD25004', 'name': 'Rahul chau'},
        ],
        '12B': [
            {'id': 'STD25003', 'name': 'Aman Verma'},
            {'id': 'STD25004', 'name': 'Priya Singh'},
        ],
    }

    selected_class = request.GET.get('class', '12A')  # Default to '12A'
    students = class_data.get(selected_class, [])

    print(selected_class)


    if request.method == 'POST':
        student_ids = request.POST.getlist('student_id')
        for sid in student_ids:
            assignment = request.POST.get(f'assignment_{sid}')
            project = request.POST.get(f'project_{sid}')
            viva = request.POST.get(f'viva_{sid}')
            remark = request.POST.get(f'remarks_{sid}')
            print(f"Student ID: {sid}")
            print(f"Assignment: {assignment}, Project: {project}, Viva: {viva}, Remark: {remark}")

        messages.success(request, "Evaluation submitted successfully!")
        return redirect(f"{reverse('teacher_evaluation')}?class={selected_class}")

    context = {
        'students': students,
        'selected_class': selected_class,
        'available_classes': class_data.keys(),
    }
    return render(request, 'school/teacher/evaluation.html', context)


def teacher_upload_marks(request):

    # Dummy data for demo (replace with actual DB calls)
    TEACHER_ASSIGNED_CLASSES = ['Class 12', 'Class 11']
    TEACHER_ASSIGNED_SUBJECTS = {
    'Class 12': ['Physics', 'Math'],
    'Class 11': ['Chemistry']
}
    EXAM_TYPES = ['P-1', 'P-2', 'P-3', 'Mid-Term', 'Yearly']

    STUDENTS_BY_CLASS = {
    'Class 12': [
        {'id': 'STD25001', 'name': 'Ayush Patel'},
        {'id': 'STD25002', 'name': 'Riya Sharma'},
    ],
    'Class 11': [
        {'id': 'STD25003', 'name': 'Aman Verma'},
    ]
}
    selected_class = request.GET.get('selected_class')
    selected_subject = request.GET.get('selected_subject')
    selected_exam = request.GET.get('selected_exam')

    students = []
    if selected_class:
        students = STUDENTS_BY_CLASS.get(selected_class, [])

    if request.method == 'POST':
        # Get class, subject, and exam from hidden inputs
        selected_class = request.POST.get('selected_class')
        selected_subject = request.POST.get('selected_subject')
        selected_exam = request.POST.get('selected_exam')

        student_ids = request.POST.getlist('student_ids')

        print(f"Class : {selected_class} | Subject : {selected_subject} | Exam : {selected_exam}")
        for student_id in student_ids:
            marks_key = f"{student_id}_marks"
            marks = request.POST.get(marks_key)
            # print(f"[INFO] Class: {selected_class}, Subject: {selected_subject}, Exam: {selected_exam}")
            print(f"Student: {student_id}, Marks: {marks}")
            # TODO: Save to database
        messages.success(request, "Marks submitted successfully!")
        return redirect('upload_marks')

    context = {
        'classes': TEACHER_ASSIGNED_CLASSES,
        'subjects': TEACHER_ASSIGNED_SUBJECTS.get(selected_class, []),
        'selected_class': selected_class,
        'selected_subject': selected_subject,
        'selected_exam': selected_exam,
        'students': students,
        'exam_types': EXAM_TYPES,
    }
    return render(request, 'school/teacher/upload_marks.html', context)


def teacher_notices(request):
    notices = [
        {'title': 'Meeting Reminder', 'date': date(2025, 7, 5), 'description': 'All staff are requested to attend the academic planning meeting tomorrow at 10 AM.'},
        {'title': 'Exam Schedule Update', 'date': date(2025, 7, 2), 'description': 'Mid Term exams will start from July 15. The updated schedule has been shared.'},
        {'title': 'Mark Entry Deadline', 'date': date(2025, 6, 28), 'description': 'All subject teachers must upload marks before July 10.'},
    ]
    return render(request, 'school/teacher/notices.html', {'notices': notices})


def teacher_schedule(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'teacher':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    print(request.path)
    schedule = [
    {'day': 'Monday', 'period': '1', 'time': '9:00–9:45 AM', 'class_name': '12A', 'subject': 'Physics', 'room': '102'},
    {'day': 'Monday', 'period': '2', 'time': '9:45–10:30 AM', 'class_name': '11B', 'subject': 'Chemistry', 'room': '103'},
    # Add more entries...
    ]
    return render(request, 'school/teacher/schedule.html', {'schedule': schedule})


def teacher_study_material(request):
    if not request.session.get('user_id') or request.session.get('user_type') != 'teacher':
        return redirect('login')  # Or use your login URL name
    print("Session:", request.session.get('user_id'))
    print(request.path)
    return render(request, 'school/teacher/study_material.html')






# ------------------------------- Teacher Dashboard Views Ends ------------------------------------------

def logout(request):
    request.session.flush()  # 🧨 Clear all session data
    return redirect('login')  # 🔁 Redirect to login page