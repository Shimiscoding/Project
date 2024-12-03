from django import forms
from .models import Student, Parent

class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'student_id', 'gender', 'date_of_birth', 'student_class', 
                  'religion', 'joining_date', 'mobile_number', 'admission_number', 'section', 'student_image']

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("A student with this ID already exists.")
        return student_id

class AddParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['father_name', 'father_email', 'mother_email']

    def clean_father_email(self):
        email = self.cleaned_data['father_email']
        if Parent.objects.filter(father_email=email).exists():
            raise forms.ValidationError("A parent with this father's email already exists.")
        return email

    def clean_mother_email(self):
        email = self.cleaned_data['mother_email']
        if Parent.objects.filter(mother_email=email).exists():
            raise forms.ValidationError("A parent with this mother's email already exists.")
        return email