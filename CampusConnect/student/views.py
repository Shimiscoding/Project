from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.contrib import messages
from school.views import create_announcement 
from django.contrib.auth import get_user_model

# Create your views here.

def add_student(request):
    if request.method == "POST":
        # Collect student data from form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_course = request.POST.get('student_course')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image', None)

        # Save parent information
        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_mobile = request.POST.get('father_mobile')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_mobile = request.POST.get('mother_mobile')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        # Perform uniqueness checks
        if Student.objects.filter(student_id=student_id).exists():
            messages.error(request, "A student with this ID already exists.")
            return redirect('add_student')  # Redirect to form page again

        # Save parent information
        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            present_address=present_address,
            permanent_address=permanent_address
        )

        # Save student information
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_course=student_course,
            religion=religion,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent
        )

        # Create the user account for the student
        user = get_user_model().objects.create_user(
            username=student.student_id,  # Using student ID as username
            password='*Student123',  # Default password (will be hashed)
            email=f"{student.student_id}@school.com",  # Email based on student ID
            first_name=student.first_name,
            last_name=student.last_name,
            is_student=True,
        )

        # Link user account to student
        student.user = user
        student.save()

        # Return success message
        messages.success(request, "Student added and account created successfully.")
        return render(request, "students/add-student.html", {'student_email': user.email})

    return render(request, "students/add-student.html")

def student_list(request):
    student_list = Student.objects.select_related('parent').all()
    unread_notification = request.user.notification_set.filter(is_read=False)
    context = {
        'student_list': student_list,
        'unread_notification': unread_notification
    }
    return render(request, "students/student.html", context)


def edit_student(request, slug):
    student = get_object_or_404(Student, slug=slug)
    parent = student.parent if hasattr(student, 'parent') else None

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        student_id = request.POST.get('student_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        student_course = request.POST.get('student_course')
        religion = request.POST.get('religion')
        joining_date = request.POST.get('joining_date')
        mobile_number = request.POST.get('mobile_number')
        admission_number = request.POST.get('admission_number')
        section = request.POST.get('section')
        student_image = request.FILES.get('student_image') if request.FILES.get('student_image') else student.student_image

        # Only check student ID uniqueness if it's changed
        if student.student_id != student_id and Student.objects.filter(student_id=student_id).exists():
            messages.error(request, "A student with this ID already exists.")
            return render(request, "students/edit-student.html", {'student': student, 'parent': parent})

        # Only check admission number uniqueness if it's changed
        if student.admission_number != admission_number and Student.objects.filter(admission_number=admission_number).exists():
            messages.error(request, "The admission number must be unique.")
            return render(request, "students/edit-student.html", {'student': student, 'parent': parent})

  

        # Update parent information
        parent.father_name = request.POST.get('father_name')
        parent.father_occupation = request.POST.get('father_occupation')
        parent.father_mobile = request.POST.get('father_mobile')
        parent.mother_name = request.POST.get('mother_name')
        parent.mother_occupation = request.POST.get('mother_occupation')
        parent.mother_mobile = request.POST.get('mother_mobile')
        parent.present_address = request.POST.get('present_address')
        parent.permanent_address = request.POST.get('permanent_address')
        parent.save()

        # Update student information
        student.first_name = first_name
        student.last_name = last_name
        student.student_id = student_id
        student.gender = gender
        student.date_of_birth = date_of_birth
        student.student_course = student_course
        student.religion = religion
        student.joining_date = joining_date
        student.mobile_number = mobile_number
        student.admission_number = admission_number
        student.section = section
        student.student_image = student_image
        student.save()

        create_announcement(request.user, f"Updated Student: {student.first_name} {student.last_name}")
        messages.success(request, "Student details updated successfully.")
        return redirect("student_list") 

    return render(request, "students/edit-student.html", {'student': student, 'parent': parent})


def view_student(request, slug):
    student = get_object_or_404(Student, student_id = slug)
    context = {
        'student': student
    }
    return render(request, "students/student-details.html", context)



def delete_student(request, slug):
    try:
        student = Student.objects.get(slug=slug)
        student.delete()  # Delete the student
        messages.success(request, 'Student deleted successfully.')
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')

    return redirect('student_list')  # Redirect to student list or other page