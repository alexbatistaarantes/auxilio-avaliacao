from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
            submission.full_clean()
            submission.save()
        return Response({'status': 200})

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
        answer.save(update_fields=['group'])
    return Response(AnswerGroupSerializer(group).data)
