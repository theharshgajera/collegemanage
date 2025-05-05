from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from app.models import Course, Session_Year, CustomUser, Student, Staff, Subject, Staff_Notification, Staff_leave, Staff_Feedback, Student_Notification, Student_Feedback, Student_leave, Attendance, Attendance_Report, Parent
from django.contrib import messages
from django.http import JsonResponse

@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    parent_count = Parent.objects.all().count()
    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()
    pending_staff_leaves = Staff_leave.objects.filter(status=0).count()
    pending_student_leaves = Student_leave.objects.filter(status=0).count()
    context = {
        'student_count': student_count,
        'staff_count': staff_count,
        'course_count': course_count,
        'subject_count': subject_count,
        'parent_count': parent_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
        'pending_staff_leaves': pending_staff_leaves,
        'pending_student_leaves': pending_student_leaves,
    }
    return render(request, 'Hod/home.html', context)

@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        full_name = request.POST.get('full_name')
        enrollment_no = request.POST.get('enrollment_no')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        semester = request.POST.get('semester')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken')
            return redirect('add_student')
        if Student.objects.filter(enrollment_no=enrollment_no).exists():
            messages.warning(request, 'Enrollment Number Is Already Taken')
            return redirect('add_student')
        user = CustomUser(
            first_name=full_name,
            last_name='',
            username=username,
            email=email,
            profile_pic=profile_pic,
            user_type=3
        )
        user.set_password(password)
        user.save()
        course = Course.objects.get(id=course_id)
        session_year = Session_Year.objects.get(id=session_year_id)
        student = Student(
            admin=user,
            address=address,
            session_year_id=session_year,
            course_id=course,
            gender=gender,
            enrollment_no=enrollment_no,
            semester=semester if semester else None
        )
        student.save()
        messages.success(request, f"{user.first_name} Successfully Added!")
        return redirect('add_student')
    context = {
        'course': course,
        'session_year': session_year,
    }
    return render(request, 'Hod/add_student.html', context)

@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()
    context = {
        'student': student,
    }
    return render(request, 'Hod/view_student.html', context)

@login_required(login_url='/')
def EDIT_STUDENT(request, id):
    student = Student.objects.get(id=id)
    course = Course.objects.all()
    session_year = Session_Year.objects.all()
    context = {
        'student': student,
        'course': course,
        'session_year': session_year,
    }
    return render(request, 'Hod/edit_student.html', context)

@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        full_name = request.POST.get('full_name')
        enrollment_no = request.POST.get('enrollment_no')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        semester = request.POST.get('semester')
        
        user = CustomUser.objects.get(id=student_id)
        user.first_name = full_name
        user.last_name = ''
        user.email = email
        user.username = username
        if password and password.strip():
            user.set_password(password)
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()
        
        student = Student.objects.get(admin=student_id)
        if enrollment_no != student.enrollment_no and Student.objects.filter(enrollment_no=enrollment_no).exists():
            messages.warning(request, 'Enrollment Number Is Already Taken')
            return redirect('edit_student', id=student.id)
        
        student.address = address
        student.gender = gender
        student.enrollment_no = enrollment_no
        course = Course.objects.get(id=course_id)
        student.course_id = course
        session_year = Session_Year.objects.get(id=session_year_id)
        student.session_year_id = session_year
        student.semester = int(semester) if semester else None
        student.save()
        messages.success(request, 'Record Successfully Updated!')
        return redirect('view_student')
    return render(request, 'Hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request, admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.success(request, 'Record Successfully Deleted!')
    return redirect('view_student')

@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        course = Course(name=course_name)
        course.save()
        messages.success(request, 'Course Successfully Created')
        return redirect('view_course')
    return render(request, 'Hod/add_course.html')

@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        'course': course,
    }
    return render(request, 'Hod/view_course.html', context)

@login_required(login_url='/')
def EDIT_COURSE(request, id):
    course = Course.objects.get(id=id)
    context = {
        'course': course,
    }
    return render(request, 'Hod/edit_course.html', context)

@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == "POST":
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)
        course.name = name
        course.save()
        messages.success(request, 'Course Successfully Updated')
        return redirect('view_course')
    return render(request, 'Hod/edit_course.html')

@login_required(login_url='/')
def DELETE_COURSE(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    messages.success(request, 'Course Successfully Deleted')
    return redirect('view_course')

@login_required(login_url='/')
def ADD_STAFF(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        subject_id = request.POST.get('subject_id')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken!')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken!')
            return redirect('add_staff')
        if subject_id and Staff.objects.filter(subjects__id=subject_id).exists():
            messages.error(request, 'This subject is already assigned to another staff member.')
            return redirect('add_staff')
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            profile_pic=profile_pic,
            user_type=2
        )
        user.set_password(password)
        user.save()
        staff = Staff(
            admin=user,
            address=address,
            gender=gender
        )
        staff.save()
        if subject_id:
            try:
                subject = Subject.objects.get(id=subject_id)
                staff.subjects.add(subject)
            except Subject.DoesNotExist:
                messages.error(request, f"Subject with ID {subject_id} does not exist.")
                return redirect('add_staff')
        messages.success(request, 'Staff Successfully Added!')
        return redirect('add_staff')
    context = {
        'subjects': subjects,
        'courses': courses,
    }
    return render(request, 'Hod/add_staff.html', context)

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        'staff': staff,
    }
    return render(request, 'Hod/view_staff.html', context)

@login_required(login_url='/')
def EDIT_STAFF(request, id):
    staff = Staff.objects.get(id=id)
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    context = {
        'staff': staff,
        'subjects': subjects,
        'courses': courses,
    }
    return render(request, 'Hod/edit_staff.html', context)

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        subject_id = request.POST.get('subject_id')
        user = CustomUser.objects.get(id=staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password and password.strip():
            user.set_password(password)
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()
        staff = Staff.objects.get(admin=staff_id)
        staff.gender = gender
        staff.address = address
        if subject_id:
            existing_staff = Staff.objects.filter(subjects__id=subject_id).exclude(id=staff.id)
            if existing_staff.exists():
                messages.error(request, 'This subject is already assigned to another staff member.')
                return redirect('edit_staff', id=staff.id)
        staff.subjects.clear()
        if subject_id:
            try:
                subject = Subject.objects.get(id=subject_id)
                staff.subjects.add(subject)
            except Subject.DoesNotExist:
                messages.error(request, f"Subject with ID {subject_id} does not exist.")
                return redirect('edit_staff', id=staff.id)
        staff.save()
        messages.success(request, 'Staff Successfully Updated')
        return redirect('view_staff')
    return render(request, 'Hod/edit_staff.html')

@login_required(login_url='/')
def DELETE_STAFF(request, admin):
    staff = CustomUser.objects.get(id=admin)
    staff.delete()
    messages.success(request, 'Record Successfully Deleted!')
    return redirect('view_staff')

@login_required(login_url='/')
def ADD_PARENT(request):
    students = Student.objects.all()
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')
        relationship = request.POST.get('relationship')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email Is Already Taken!')
            return redirect('add_parent')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken!')
            return redirect('add_parent')
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            profile_pic=profile_pic,
            user_type=4
        )
        user.set_password(password)
        user.save()
        student = Student.objects.get(id=student_id)
        parent = Parent(
            admin=user,
            student=student,
            relationship=relationship,
            phone_number=phone_number,
            address=address
        )
        parent.save()
        messages.success(request, 'Parent Added Successfully!')
        return redirect('add_parent')
    context = {
        'students': students,
    }
    return render(request, 'Hod/add_parent.html', context)

@login_required(login_url='/')
def VIEW_PARENT(request):
    parents = Parent.objects.all()
    context = {
        'parents': parents,
    }
    return render(request, 'Hod/view_parent.html', context)

@login_required(login_url='/')
def EDIT_PARENT(request, id):
    parent = Parent.objects.get(id=id)
    students = Student.objects.all()
    context = {
        'parent': parent,
        'students': students,
    }
    return render(request, 'Hod/edit_parent.html', context)

@login_required(login_url='/')
def UPDATE_PARENT(request):
    if request.method == "POST":
        parent_id = request.POST.get('parent_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id')
        relationship = request.POST.get('relationship')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        user = CustomUser.objects.get(id=parent_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        if password and password.strip():
            user.set_password(password)
        if profile_pic:
            user.profile_pic = profile_pic
        user.save()
        parent = Parent.objects.get(admin=parent_id)
        student = Student.objects.get(id=student_id)
        parent.student = student
        parent.relationship = relationship
        parent.phone_number = phone_number
        parent.address = address
        parent.save()
        messages.success(request, 'Parent Updated Successfully!')
        return redirect('view_parent')
    return render(request, 'Hod/edit_parent.html')

@login_required(login_url='/')
def DELETE_PARENT(request, admin):
    parent = CustomUser.objects.get(id=admin)
    parent.delete()
    messages.success(request, 'Parent Deleted Successfully!')
    return redirect('view_parent')

@login_required(login_url='/')
def ADD_SUBJECT(request):
    courses = Course.objects.all()
    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        course_id = request.POST.get('course_id')
        credit = request.POST.get('credit')
        try:
            course = Course.objects.get(id=course_id)
            if subject_code and Subject.objects.filter(subject_code=subject_code).exists():
                messages.error(request, 'Subject Code is already taken.')
                return redirect('add_subject')
            subject = Subject(
                name=subject_name,
                subject_code=subject_code,
                course=course,
                credit=int(credit) if credit else None
            )
            subject.save()
            messages.success(request, 'Subject Successfully Added!')
            return redirect('add_subject')
        except Course.DoesNotExist:
            messages.error(request, "Selected course does not exist.")
            return redirect('add_subject')
    context = {
        'courses': courses,
    }
    return render(request, 'Hod/add_subject.html', context)

@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all()
    context = {
        'subject': subject,
    }
    return render(request, 'Hod/view_subject.html', context)

@login_required(login_url='/')
def EDIT_SUBJECT(request, id):
    subject = Subject.objects.get(id=id)
    course = Course.objects.all()
    context = {
        'subject': subject,
        'course': course,
    }
    return render(request, 'Hod/edit_subject.html', context)

@login_required(login_url='/')
def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        course_id = request.POST.get('course_id')
        credit = request.POST.get('credit')
        try:
            course = Course.objects.get(id=course_id)
            subject = Subject.objects.get(id=subject_id)
            if subject_code and subject_code != subject.subject_code and Subject.objects.filter(subject_code=subject_code).exists():
                messages.error(request, 'Subject Code is already taken.')
                return redirect('edit_subject', id=subject_id)
            subject.name = subject_name
            subject.subject_code = subject_code
            subject.course = course
            subject.credit = int(credit) if credit else None
            subject.save()
            messages.success(request, 'Subject Successfully Updated!')
            return redirect('view_subject')
        except Course.DoesNotExist:
            messages.error(request, "Selected course does not exist.")
            return redirect('edit_subject', id=subject_id)
        except Subject.DoesNotExist:
            messages.error(request, "Subject does not exist.")
            return redirect('view_subject')
    return render(request, 'Hod/edit_subject.html')

@login_required(login_url='/')
def DELETE_SUBJECT(request, id):
    subject = Subject.objects.get(id=id)
    subject.delete()
    messages.success(request, 'Subject Successfully Deleted!')
    return redirect('view_subject')

@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == "POST":
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')
        session = Session_Year(
            session_start=session_year_start,
            session_end=session_year_end,
        )
        session.save()
        messages.success(request, 'Session Successfully Created')
        return redirect('add_session')
    return render(request, 'Hod/add_session.html')

@login_required(login_url='/')
def VIEW_SESSION(request):
    session = Session_Year.objects.all()
    context = {
        'session': session,
    }
    return render(request, 'Hod/view_session.html', context)

@login_required(login_url='/')
def EDIT_SESSION(request, id):
    session = Session_Year.objects.get(id=id)
    context = {
        'session': session,
    }
    return render(request, 'Hod/edit_session.html', context)

@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')
        session = Session_Year.objects.get(id=session_id)
        session.session_start = session_year_start
        session.session_end = session_year_end
        session.save()
        messages.success(request, 'Session Successfully Updated!')
        return redirect('view_session')
    return render(request, 'Hod/edit_session.html')

@login_required(login_url='/')
def DELETE_SESSION(request, id):
    session = Session_Year.objects.get(id=id)
    session.delete()
    messages.success(request, 'Session Successfully Deleted!')
    return redirect('view_session')

@login_required(login_url='/')
def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[:5]
    context = {
        'staff': staff,
        'see_notification': see_notification,
    }
    return render(request, 'Hod/staff_notification.html', context)

@login_required(login_url='/')
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')
        staff = Staff.objects.get(admin=staff_id)
        notification = Staff_Notification(
            staff_id=staff,
            message=message,
        )
        notification.save()
        messages.success(request, 'Notification Successfully Sent')
        return redirect('staff_send_notification')

@login_required(login_url='/')
def STAFF_LEAVE_VIEW(request):
    staff_leave = Staff_leave.objects.all()
    context = {
        'staff_leave': staff_leave,
    }
    return render(request, 'Hod/staff_leave.html', context)

@login_required(login_url='/')
def STAFF_APPROVE_LEAVE(request, id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    staff = leave.staff_id
    message = f"Your leave application for {leave.date} has been approved."
    notification = Staff_Notification(staff_id=staff, message=message)
    notification.save()
    messages.success(request, 'Leave Approved and Notification Sent!')
    return redirect('staff_leave_view')

@login_required(login_url='/')
def STAFF_DISAPPROVE_LEAVE(request, id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    staff = leave.staff_id
    message = f"Your leave application for {leave.date} has been rejected."
    notification = Staff_Notification(staff_id=staff, message=message)
    notification.save()
    messages.success(request, 'Leave Disapproved and Notification Sent!')
    return redirect('staff_leave_view')

@login_required(login_url='/')
def STUDENT_LEAVE_VIEW(request):
    student_leave = Student_leave.objects.all()
    context = {
        'student_leave': student_leave,
    }
    return render(request, 'Hod/student_leave.html', context)

@login_required(login_url='/')
def STUDENT_APPROVE_LEAVE(request, id):
    student_leave = Student_leave.objects.get(id=id)
    student_leave.status = 1
    student_leave.save()
    student = student_leave.student_id
    message = f"Your leave application for {student_leave.date} has been approved."
    notification = Student_Notification(student_id=student, message=message)
    notification.save()
    messages.success(request, 'Leave Approved and Notification Sent!')
    return redirect('student_leave_view')

@login_required(login_url='/')
def STUDENT_DISAPPROVE_LEAVE(request, id):
    student_leave = Student_leave.objects.get(id=id)
    student_leave.status = 2
    student_leave.save()
    student = student_leave.student_id
    message = f"Your leave application for {student_leave.date} has been rejected."
    notification = Student_Notification(student_id=student, message=message)
    notification.save()
    messages.success(request, 'Leave Disapproved and Notification Sent!')
    return redirect('student_leave_view')

@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    feedback = Staff_Feedback.objects.all()
    feedback_history = Staff_Feedback.objects.all().order_by('-id')[:5]
    context = {
        'feedback': feedback,
        'feedback_history': feedback_history,
    }
    return render(request, 'Hod/staff_feedback.html', context)

@login_required(login_url='/')
def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')
        try:
            feedback = Staff_Feedback.objects.get(id=feedback_id)
            feedback.feedback_reply = feedback_reply
            feedback.status = 1
            feedback.save()
            messages.success(request, 'Reply Sent Successfully!')
            feedback_list = Staff_Feedback.objects.all()
            feedback_history = Staff_Feedback.objects.all().order_by('-id')[:5]
            context = {
                'feedback': feedback_list,
                'feedback_history': feedback_history,
            }
            return render(request, 'Hod/staff_feedback.html', context)
        except Staff_Feedback.DoesNotExist:
            messages.error(request, 'Feedback not found.')
            feedback_list = Staff_Feedback.objects.all()
            feedback_history = Staff_Feedback.objects.all().order_by('-id')[:5]
            context = {
                'feedback': feedback_list,
                'feedback_history': feedback_history,
            }
            return render(request, 'Hod/staff_feedback.html', context)
    return redirect('staff_feedback')

@login_required(login_url='/')
def STUDENT_FEEDBACK(request):
    feedback = Student_Feedback.objects.all()
    feedback_history = Student_Feedback.objects.all().order_by('-id')[:5]
    context = {
        'feedback': feedback,
        'feedback_history': feedback_history,
    }
    return render(request, 'Hod/student_feedback.html', context)

@login_required(login_url='/')
def REPLY_STUDENT_FEEDBACK(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')
        try:
            feedback = Student_Feedback.objects.get(id=feedback_id)
            feedback.feedback_reply = feedback_reply
            feedback.status = 1
            feedback.save()
            messages.success(request, 'Reply Sent Successfully!')
            feedback_list = Student_Feedback.objects.all()
            feedback_history = Student_Feedback.objects.all().order_by('-id')[:5]
            context = {
                'feedback': feedback_list,
                'feedback_history': feedback_history,
            }
            return render(request, 'Hod/student_feedback.html', context)
        except Student_Feedback.DoesNotExist:
            messages.error(request, 'Feedback not found.')
            feedback_list = Student_Feedback.objects.all()
            feedback_history = Student_Feedback.objects.all().order_by('-id')[:5]
            context = {
                'feedback': feedback_list,
                'feedback_history': feedback_history,
            }
            return render(request, 'Hod/student_feedback.html', context)
    return redirect('student_feedback')

@login_required(login_url='/')
def STUDENT_SEND_NOTIFICATION(request):
    student = Student.objects.all()
    notification = Student_Notification.objects.all()
    context = {
        'student': student,
        'notification': notification,
    }
    return render(request, 'Hod/student_notification.html', context)

@login_required(login_url='/')
def SAVE_STUDENT_NOTIFICATION(request):
    if request.method == "POST":
        message = request.POST.get('message')
        student_id = request.POST.get('student_id')
        student = Student.objects.get(admin=student_id)
        stud_notification = Student_Notification(
            student_id=student,
            message=message,
        )
        stud_notification.save()
        messages.success(request, 'Student Notification Successfully Sent')
        return redirect('student_send_notification')

@login_required(login_url='/')
def VIEW_ATTENDANCE(request):
    subjects = Subject.objects.all()
    session_years = Session_Year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    start_date = request.GET.get('start_date') or request.POST.get('start_date')
    end_date = request.GET.get('end_date') or request.POST.get('end_date')
    attendance_reports = None

    if action == 'view_attendance' and request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')

        try:
            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            
            attendance = Attendance.objects.filter(
                subject_id=get_subject,
                session_year_id=get_session_year
            )
            
            if start_date:
                attendance = attendance.filter(attendance_data__gte=start_date)
            if end_date:
                attendance = attendance.filter(attendance_data__lte=end_date)
                
            attendance_reports = Attendance_Report.objects.filter(
                attendance_id__in=attendance
            ).order_by('attendance_id__attendance_data', 'student_id__admin__first_name')

        except (Subject.DoesNotExist, Session_Year.DoesNotExist):
            messages.error(request, "Invalid subject or session year selected.")
            return redirect('view_attendance')

    if request.GET.get('download') == 'csv':
        try:
            subject_id = request.GET.get('subject_id')
            session_year_id = request.GET.get('session_year_id')
            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            
            attendance = Attendance.objects.filter(
                subject_id=get_subject,
                session_year_id=get_session_year
            )
            
            if start_date:
                attendance = attendance.filter(attendance_data__gte=start_date)
            if end_date:
                attendance = attendance.filter(attendance_data__lte=end_date)
                
            attendance_reports = Attendance_Report.objects.filter(
                attendance_id__in=attendance
            ).order_by('attendance_id__attendance_data', 'student_id__admin__first_name')

            if attendance_reports:
                response = HttpResponse(content_type='text/csv')
                filename = f'attendance_{get_subject.name}_{start_date or "all"}_to_{end_date or "all"}.csv'
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                
                writer = csv.writer(response)
                writer.writerow(['Student ID', 'Student Name', 'Subject', 'Date', 'Status'])
                
                for report in attendance_reports:
                    writer.writerow([
                        report.student_id.admin.id,
                        f"{report.student_id.admin.first_name} {report.student_id.admin.last_name}",
                        report.attendance_id.subject_id.name,
                        report.attendance_id.attendance_data.strftime('%Y-%m-%d'),
                        "Present" if report.status == 1 else "Absent"
                    ])
                
                return response
            else:
                messages.error(request, "No attendance data available to export.")
                return redirect('view_attendance')
                
        except (Subject.DoesNotExist, Session_Year.DoesNotExist):
            messages.error(request, "Invalid subject or session year selected.")
            return redirect('view_attendance')

    context = {
        'subjects': subjects,
        'session_years': session_years,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'start_date': start_date,
        'end_date': end_date,
        'attendance_reports': attendance_reports,
    }
    return render(request, 'Hod/view_attendance.html', context)

@login_required(login_url='/')
def get_subjects_by_course(request):
    course_id = request.GET.get('course_id')
    if course_id:
        subjects = Subject.objects.filter(course_id=course_id).values('id', 'name')
        return JsonResponse({'subjects': list(subjects)})
    return JsonResponse({'subjects': []})

# Add these imports at the top
import csv
import io
from django.http import HttpResponse

# Add these new views
@login_required(login_url='/')
def BULK_ADD_STUDENT(request):
    if request.method == "POST":
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, 'Please upload a CSV file')
            return redirect('bulk_add_student')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File must be a CSV')
            return redirect('bulk_add_student')

        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.DictReader(io.StringIO(decoded_file))
        
        success_count = 0
        error_count = 0
        
        for row in csv_data:
            try:
                # Check if user already exists
                if CustomUser.objects.filter(email=row['email']).exists():
                    error_count += 1
                    continue
                if CustomUser.objects.filter(username=row['username']).exists():
                    error_count += 1
                    continue
                if Student.objects.filter(enrollment_no=row['enrollment_no']).exists():
                    error_count += 1
                    continue

                # Create CustomUser
                user = CustomUser(
                    first_name=row['full_name'],
                    last_name='',
                    username=row['username'],
                    email=row['email'],
                    user_type=3
                )
                user.set_password(row['password'])
                user.save()

                # Get related objects
                course = Course.objects.get(id=row['course_id'])
                session_year = Session_Year.objects.get(id=row['session_year_id'])

                # Create Student
                student = Student(
                    admin=user,
                    address=row['address'],
                    session_year_id=session_year,
                    course_id=course,
                    gender=row['gender'],
                    enrollment_no=row['enrollment_no'],
                    semester=row['semester']
                )
                student.save()
                success_count += 1

            except Exception as e:
                error_count += 1
                continue

        messages.success(request, f'Successfully added {success_count} students. Failed to add {error_count} students.')
        return redirect('bulk_add_student')

    return render(request, 'Hod/bulk_add_student.html')

@login_required(login_url='/')
def DOWNLOAD_SAMPLE_CSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_students.csv"'

    writer = csv.writer(response)
    writer.writerow(['full_name', 'enrollment_no', 'email', 'username', 'password', 
                    'address', 'gender', 'course_id', 'session_year_id', 'semester'])
    writer.writerow(['John Doe', 'EN001', 'john@example.com', 'john_doe', 'password123', 
                    '123 Street', 'Male', '1', '1', '1'])

    return response

@login_required(login_url='/')
def BULK_ADD_STAFF(request):
    if request.method == "POST":
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, 'Please upload a CSV file')
            return redirect('bulk_add_staff')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File must be a CSV')
            return redirect('bulk_add_staff')

        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.DictReader(io.StringIO(decoded_file))
        
        success_count = 0
        error_count = 0
        
        for row in csv_data:
            try:
                # Check if user already exists
                if CustomUser.objects.filter(email=row['email']).exists():
                    error_count += 1
                    continue
                if CustomUser.objects.filter(username=row['username']).exists():
                    error_count += 1
                    continue

                # Create CustomUser
                user = CustomUser(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    username=row['username'],
                    user_type=2
                )
                user.set_password(row['password'])
                user.save()

                # Create Staff
                staff = Staff(
                    admin=user,
                    address=row['address'],
                    gender=row['gender']
                )
                staff.save()

                # Add subject if provided
                if row['subject_id']:
                    try:
                        subject = Subject.objects.get(id=row['subject_id'])
                        staff.subjects.add(subject)
                    except Subject.DoesNotExist:
                        pass

                success_count += 1

            except Exception as e:
                error_count += 1
                continue

        messages.success(request, f'Successfully added {success_count} staff members. Failed to add {error_count} staff members.')
        return redirect('bulk_add_staff')

    return render(request, 'Hod/bulk_add_staff.html')

@login_required(login_url='/')
def DOWNLOAD_STAFF_SAMPLE_CSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sample_staff.csv"'

    writer = csv.writer(response)
    writer.writerow(['first_name', 'last_name', 'email', 'username', 'password', 
                    'address', 'gender', 'subject_id'])
    writer.writerow(['John', 'Doe', 'john@example.com', 'john_doe', 'password123', 
                    '123 Street', 'Male', '1'])

    return response