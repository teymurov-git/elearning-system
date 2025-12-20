from django.shortcuts import render
from account.models import User, Exam, StudentResult
from django.contrib import messages

# Create your views here.


def home(request):
    return render(request, 'index.html')


def check_result(request):
    student = None
    student_result = None
    error = None
    exams = Exam.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        work_number = request.POST.get('work_number', '').strip()
        exam_id = request.POST.get('exam_id', '').strip()
        
        if not work_number:
            error = 'Zəhmət olmasa iş nömrəsini daxil edin.'
        elif not exam_id:
            error = 'Zəhmət olmasa sınağı seçin.'
        else:
            try:
                student = User.objects.get(work_number=work_number)
                try:
                    exam = Exam.objects.get(id=exam_id)
                    student_result = StudentResult.objects.filter(student=student, exam=exam).first()
                    if not student_result:
                        error = f'{exam.name} üçün nəticə tapılmadı.'
                except Exam.DoesNotExist:
                    error = 'Seçilmiş sınaq tapılmadı.'
            except User.DoesNotExist:
                error = 'Bu iş nömrəsi ilə tələbə tapılmadı.'
            except User.MultipleObjectsReturned:
                student = User.objects.filter(work_number=work_number).first()
                try:
                    exam = Exam.objects.get(id=exam_id)
                    student_result = StudentResult.objects.filter(student=student, exam=exam).first()
                    if not student_result:
                        error = f'{exam.name} üçün nəticə tapılmadı.'
                except Exam.DoesNotExist:
                    error = 'Seçilmiş sınaq tapılmadı.'
    
    return render(request, 'check_result.html', {
        'student': student,
        'student_result': student_result,
        'exams': exams,
        'error': error
    })