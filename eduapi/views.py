from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .serializers import *
from .models import *
from django.db.models import Max

from utils import ViewUtil


class CourseApi(APIView):
    permission_classes = (IsAuthenticated, )
    
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        return self.obj.get(request, Course, CourseListSerializer, CourseSerializer, 'Course')
    
    def post(self, request):
        return self.obj.post(request, CourseSerializer, 'Course created', '/course')
    
    def put(self, request):
        return self.obj.put(request, Course, CourseSerializer, 'Course updated', '/course')
    
    def delete(self, request):
        return self.obj.delete(request, Course, 'Course', '/course')


class StudentApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        return self.obj.get(request, Student, StudentListSerializer, StudentDetailSerializer, 'Student')
    
    def post(self, request):
        try:
            request.data._mutable = True
        except Exception as e:
            self.obj.prin(e)

        request.data.update({'is_registerd': True})
        return self.obj.post(request, StudentSerializer, 'Student registerd', '/student')
    
    def put(self, request):
        if request.FILES:
            try:
                request.data._mutable = True
            except Exception as e:
                self.obj.prin(e)

            request.data.update({'is_registerd': True})
            return self.obj.put(request, Student, StudentSerializer, 'Student updated', '/student')
        else:
            try:
                request.data._mutable = True
            except Exception as e:
                self.obj.prin(e)

            request.data.update({'is_registerd': True})
            return self.obj.put(request, Student, StudentWithoutPhotoSerializer, 'Student updated', '/student')
    
    def delete(self, request):
        return self.obj.delete(request, Student, 'Student', '/student')


class EnrollApi(APIView):
    # permission_classes = (IsAuthenticated, )
    
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        get_data = Student.objects.filter(id=request.GET.get('id'), enroll_number=None).values('name', 'reg_year')
        if get_data.exists():
            return_str = get_data[0]['name']

            generated_number = self.create_enroll(get_data[0]['reg_year'])

            get_data.update(enroll_number=generated_number, is_enrolled=True)
            msg = f'{return_str}\'s enroll has been generated successfully.'
            resp = {
                **{'status': status.HTTP_200_OK},
                **self.obj.resp_fun(msg, '/student', 'success')
            }
        else:
            msg = f'Student data not found'
            resp = {
                **{'status': status.HTTP_404_NOT_FOUND},
                **self.obj.resp_fun(msg, '/student', 'error')
            }
        
        return Response(resp)

    def create_enroll(self, year):
        get_data = Student.objects.filter(Q(reg_year=year), ~Q(enroll_number=None)).aggregate(Max('enroll_number'))
        
        if get_data['enroll_number__max']:
            return f"CIMS-{year}/{'%04d' % ((int(get_data['enroll_number__max'].split('/')[1]) + 1),)}"
        else:
            return f"CIMS-{year}/{'%04d' % (1,)}"


class NonExamineeAPI(APIView):
    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        if bool(dict(request.GET)):
            examinee = Student.objects.filter(is_examinee=0, id=request.GET.get('id'))
            resp = StudentDetailSerializer(examinee, many=False).data
        else:
            non_examinee = Student.objects.filter(is_examinee=0)
            resp = StudentListSerializer(non_examinee, many=True).data
        
        return Response(resp)


class ExamApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        if bool(dict(request.GET)):
            examinee = Student.objects.filter(is_examinee=1, id=request.GET.get('id'))
            if examinee[0].course.course_name.lower() == 'adca':
                resp = StudentADCAExamineeDetailSerializer(examinee[0], many=False).data
            else:
                resp = StudentDCAExamineeDetailSerializer(examinee[0], many=False).data
        else:
            examinee = Student.objects.filter(is_examinee=1)
            resp = StudentExamineeListSerializer(examinee, many=True).data
        
        return Response(resp)
    
    def post(self, request):
        resp = self.request_filter(request, 'add')
        if resp:
            msg = f'Exam marks has been added successfully.'
            resp = {
                **{'status': status.HTTP_200_OK},
                **self.obj.resp_fun(msg, '/exam', 'success')
            }
        else:
            msg = f'Exam marks has not been added.'
            resp = {
                **{'status': status.HTTP_406_NOT_ACCEPTABLE},
                **self.obj.resp_fun(msg, '', 'error')
            }
        
        return Response(resp)
    
    def put(self, request):
        resp = self.request_filter(request, 'update')
        if resp:
            msg = f'Exam marks has been updated successfully.'
            resp = {
                **{'status': status.HTTP_200_OK},
                **self.obj.resp_fun(msg, '/exam', 'success')
            }
        else:
            msg = f'Exam marks has not been updated.'
            resp = {
                **{'status': status.HTTP_406_NOT_ACCEPTABLE},
                **self.obj.resp_fun(msg, '', 'error')
            }
        
        return Response(resp)
    
    def request_filter(self, request, method):
        req = request.POST
        std = req.get('name').split('*')

        try:
            if method == 'add':
                certi_no = self.gen_certi_no(std[4].split('- ')[-1])

                if std[3].lower() == 'adca':
                    Student.objects.filter(id=std[0]).update(
                        theory_s1=req.get('theory_s1'), os=req.get('os'), pretical_s1=req.get('pretical_s1'),
                        theory_s2=req.get('theory_s2'), pretical_s2=req.get('pretical_s2'), oral_s2=req.get('oral_s2'),
                        exam_year=req.get('exam_year'), exam_month=req.get('exam_month'), is_examinee=True,
                        cretificate_no=certi_no
                    )
                else:
                    Student.objects.filter(id=std[0]).update(
                        theory_s1=req.get('theory_s1'), pretical_s1=req.get('pretical_s1'), oral_s1=req.get('oral_s1'),
                        exam_year=req.get('exam_year'), exam_month=req.get('exam_month'), is_examinee=True,
                        cretificate_no=certi_no
                    )
            else:
                if std[3].lower() == 'adca':
                    Student.objects.filter(id=std[0]).update(
                        theory_s1=req.get('theory_s1'), os=req.get('os'), pretical_s1=req.get('pretical_s1'),
                        theory_s2=req.get('theory_s2'), pretical_s2=req.get('pretical_s2'), oral_s2=req.get('oral_s2'),
                        exam_year=req.get('exam_year'), exam_month=req.get('exam_month'), is_examinee=True
                    )
                else:
                    Student.objects.filter(id=std[0]).update(
                        theory_s1=req.get('theory_s1'), pretical_s1=req.get('pretical_s1'), oral_s1=req.get('oral_s1'),
                        exam_year=req.get('exam_year'), exam_month=req.get('exam_month'), is_examinee=True
                    )
            
            return True
        except Exception as e:
            self.obj.prin(e)
            return False
    
    def gen_certi_no(self, year):
        year_numbering = {'2018': 'A', '2019': 'B', '2020': 'C', '2021': 'D', '2022': 'E', '2023': 'F', '2024': 'G', '2025': 'H'}
        get_data = Student.objects.filter(Q(reg_year=year), ~Q(cretificate_no=None)).aggregate(Max('cretificate_no'))

        if get_data['cretificate_no__max']:
            return f"C{year_numbering[year]}{'%03d' % ((int(get_data['cretificate_no__max'][2:]) + 1),)}"
        else:
            return f"C{year_numbering[year]}{'%03d' % (501,)}"


class EnableDisableCertiApi(APIView):
    # permission_classes = (IsAuthenticated, )

    def __init__(self):
        self.obj = ViewUtil()

    def get(self, request):
        toggle = True if request.GET.get('is_certi') == 'false' else False
        Student.objects.filter(id=request.GET.get('id')).update(is_certified=toggle)
        
        msg = f'Certificate has been {"Enabled" if toggle else "Disabled"} successfully.'
        resp = {
            **{'status': status.HTTP_200_OK},
            **self.obj.resp_fun(msg, '/exam', 'success'),
            **{'status': toggle}
        }
        
        return Response(resp)