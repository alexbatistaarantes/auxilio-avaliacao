from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

import xlwt

from .models import *
from .serializers import *
from .utils import get_submission_grading, send_grading_email
from .sorters import *

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SEND_EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")

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

    def update(self, request, *args, **kwargs):

        answer = self.get_object()
        answer.x = request.data['x']
        answer.y = request.data['y']
        answer.width = request.data['width']
        answer.height = request.data['height']

        answer.save(propagate = request.data['propagate'])

        serialized = AnswersSerializer(answer)

        return Response(serialized.data)

# ANSWER GROUP #
class AnswerGroupViewSet(viewsets.ModelViewSet):
    """ Grupo de Respostas
    """

    queryset = AnswerGroup.objects.all()
    serializer_class = AnswerGroupSerializer

# UPDATE ANSWERS IN A ANSWER GROUP #
@api_view(['PATCH'])
def update_answers_group(request):
    """ Altera o grupo de múltiplas Respostas
    """

    group_id = request.data['group']
    answers_ids = request.data['answers']

    if group_id is not None:
        group = get_object_or_404(AnswerGroup, pk=group_id)
    else:
        group = None
    answers = Answer.objects.filter(id__in=answers_ids)

    for answer in answers:
        answer.group = group
        answer.full_clean()
        answer.save()
    return Response(AnswerGroupSerializer(group).data)

def get_sorters(request):

    return JsonResponse(list(sorters.keys()), safe=False)

@api_view(['PATCH'])
def sort_answers(request):

    field = get_object_or_404(Field, pk=request.data['field'])
    sorter = request.data['sorter']

    sorters[sorter](field)

    return HttpResponse(status=200)

def get_assignment_grading_sheet(request, assignment_id):
    """ Cria e retorna planilha com notas e correções de todas as entregas
    """

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

def download_submission_grading(request, submission_id):
    """ Baixa PDF com correção de uma submissão
    """

    submission = get_object_or_404(Submission, pk=submission_id)

    pdf = get_submission_grading(submission)

    response = HttpResponse(bytes(pdf), content_type='application/pdf')
    response['Content-Disposition'] = f"inline; filename=\"{submission.assignment.title}-{submission.studentId}.pdf\""

    return response

def email_grading(request, assignment_id):

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    submissions = assignment.submissions

    for submission in submissions.all():
        grading = get_submission_grading(submission)
        send_grading_email(assignment, submission, grading, SEND_EMAIL, PASSWORD)

    return HttpResponse(status=200)
