from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import xlwt
import pdfkit

from .models import *
from .serializers import *

# REST API

# ASSIGNMENT #
class AssignmentViewSet(viewsets.ModelViewSet):
    """ Atividades
    """

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

# ASSIGNMENT FIELDS #
class AssignmentFieldsViewSet(viewsets.ModelViewSet):
    """ Campos de uma Atividade
    """

    serializer_class = FieldSerializer

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        return Field.objects.filter(assignment__id=assignment_id)

# ASSIGNMENT SUBMISSIONS #
class AssignmentSubmissionsViewSet(viewsets.ModelViewSet):
    """ Entregas de uma Atividade
    """

    serializer_class = SubmissionSerializer

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        return Submission.objects.filter(assignment__id=assignment_id)

# FIELD #
class FieldViewSet(viewsets.ModelViewSet):
    """ Campos
    """

    queryset = Field.objects.all()
    serializer_class = FieldSerializer

# FIELD ANSWERS #
class FieldAnswersViewSet(viewsets.ModelViewSet):
    """ Respostas de um Campo
    """

    serializer_class = AnswersSerializer

    def get_queryset(self):
        field_id = self.kwargs['field_id']
        return Answer.objects.filter(field__id=field_id)

# FIELD ANSWER GROUPS #
class FieldAnswerGroupsViewSet(viewsets.ModelViewSet):
    """ Grupos de um Campo
    """

    serializer_class = AnswerGroupSerializer

    def get_queryset(self):
        field_id = self.kwargs['field_id']
        field = get_object_or_404(Field, pk=field_id)
        return AnswerGroup.objects.filter(field=field)

# SUBMISSION #
class SubmissionViewSet(viewsets.ModelViewSet):
    """ Entregas
    """

    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def create(self, request, *args, **kwargs):
        """ Salva multiplas entregas
        """

        assignment_id = request.POST['assignment']
        assignment = Assignment.objects.get(pk=assignment_id)
        images = request.FILES.getlist('images')
        for image in images:
            submission = Submission(assignment=assignment, image=image)
            submission.clean()
            submission.save()
        return Response(SubmissionSerializer(submission).data)

# SUBMISSION ANSWERS #
class SubmissionAnswersViewSet(viewsets.ModelViewSet):
    """ Respostas de uma Entrega
    """

    serializer_class = AnswersSerializer

    def get_queryset(self):
        submission_id = self.kwargs['submission_id']
        return Answer.objects.filter(submission__id=submission_id)

# ANSWER #
class AnswerViewSet(viewsets.ModelViewSet):
    """ Resposta
    """

    queryset = Answer.objects.all()
    serializer_class = AnswersSerializer

# ANSWER GROUP #
class AnswerGroupViewSet(viewsets.ModelViewSet):
    queryset = AnswerGroup.objects.all()
    serializer_class = AnswerGroupSerializer

# UPDATE ANSWERS IN A ANSWER GROUP #
@api_view(['PATCH'])
def update_answers_group(request):
    """ Altera o grupo de múltiplas Respostas
    """

    group_id = request.data['group']
    answers_id = request.data['answers']

    if group_id is not None:
        group = get_object_or_404(AnswerGroup, pk=group_id)
    else:
        group = None
    answers = Answer.objects.filter(id__in=answers_id)

    for answer in answers:
        answer.group = group
        answer.full_clean()
        answer.save()
    return Response(AnswerGroupSerializer(group).data)

def get_assignment_grading_sheet(request, assignment_id):

    assignment = get_object_or_404(Assignment, pk=assignment_id)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attatchment; filename="grading.xls"'

    workbook = xlwt.Workbook(encoding='utf-8')
    
    # Notas dos alunos
    points_sheet = workbook.add_sheet('Notas')
    points_sheet.write(0, 0, 'Aluno')
    points_sheet.write(0, 1, f"Nota (total {assignment.total_points})")
    
    # Correção
    grading_sheet = workbook.add_sheet('Correção')
    grading_sheet.write(0, 0, 'Aluno')
    grading_sheet.write(0, 1, 'Questão')
    grading_sheet.write(0, 2, 'Valor da Questão')
    grading_sheet.write(0, 3, 'Pontos')
    grading_sheet.write(0, 4, 'Comentário')

    points_row = 1
    grading_row = 1    
    submissions = Submission.objects.filter(assignment=assignment)
    for submission in submissions:
        points_sheet.write(points_row, 0, submission.studentId)
        points_sheet.write(points_row, 1, submission.total_points)
        points_row += 1 

        for answer in submission.answers.all():
            grading_sheet.write(grading_row, 0, submission.studentId)
            grading_sheet.write(grading_row, 1, answer.field.label)
            grading_sheet.write(grading_row, 2, answer.field.points)
            grading_sheet.write(grading_row, 3, answer.points)
            grading_sheet.write(grading_row, 4, answer.feedback)
            grading_row += 1

    workbook.save(response)
    return response

def get_submission_grading_report(request, submission_id):

    submission = Submission.objects.get(pk=submission_id)

    context = {
        'submission': submission
    }
    report_html = render_to_string('auxilioavaliacao/submission_grading_report.html', context=context)

    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf = pdfkit.from_string(report_html, configuration=config)
    ## SEPARAR PAGINAS
    return HttpResponse(pdf, content_type='application/pdf')
