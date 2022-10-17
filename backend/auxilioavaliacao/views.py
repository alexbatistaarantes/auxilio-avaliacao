from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.base import ContentFile
import base64
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .forms import *
from .serializers import *

def home(request):
    """ Homepage com a lista de todas as Atividade (:model:`auxilioavalicao.Assignment`) criadas
    """

    assignments = Assignment.objects.all()
    context = { 'assignments': assignments }
    return render(request, 'auxilioavaliacao/home.html', context)

def new_assignment(request):
    """ Formulário para inserir nova atividade (:model:`auxilioavalicao.Assignment`)
    """

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save()
            return HttpResponseRedirect(reverse('auxilioavaliacao:assignment', args=[assignment.id]))
    else:
        form = AssignmentForm()

    context = {'form': form}
    return render(request, 'auxilioavaliacao/new_assignment.html', context)

def assignment(request, assignment_id):
    """ Mostra a atividade (:model:`auxilioavaliacao.Assignment`), seus campos (:model:`auxilioavaliacao.Field`), e entregas (:model:`auxilioavaliacao.Submission`)
    """

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    context = {
        'assignment': assignment
    }
    return render(request, 'auxilioavaliacao/assignment.html', context)

def new_field(request, assignment_id):
    """ Ferramenta de seleção de uma nova região que representa um campo (:model:`auxilioavaliacao.Field`) de uma atividade (:model:`auxilioavaliacao.Assignment`)
    """
    
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == "POST":
        form = FieldForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            field = Field(**data, assignment=assignment)
            field.save()

            # Salva a imagem da região a partir do campo da imagem em base64, feita pelo Croppie
            # format, file_base64 = request.POST['image_base64'].split(';base64,')
            # extension = format.split('/')[-1]
            # file = ContentFile(base64.b64decode(file_base64))
            # filename = f"{field.id}.{extension}"
            # field.file.save(filename, file, save=True)

            return HttpResponseRedirect(reverse('auxilioavaliacao:assignment', args=[assignment.id]))
    else:
        form = FieldForm()

    context = {
        'assignment': assignment,
        'form': form
    }
    return render(request, 'auxilioavaliacao/new_field.html', context)

def field(request, assignment_id, field_id):
    """ Página do campo (:model:`auxilioavaliacao.Field`)
    """

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    field = get_object_or_404(Field, pk=field_id)
    # TODO: Pegar respostas desse campo
    answers = field.answers.all() #Answer.objects.all().filter(field=field)
    context = {
        'assignment': assignment,
        'field': field,
        'answers': answers
    }
    return render(request, 'auxilioavaliacao/field.html', context)

def new_submission(request, assignment_id):
    """ Página para adicionar apenas uma nova Entrega (:model:`auxilioavaliacao.Submission`)
    """

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            submission = Submission(**data, assignment=assignment)
            submission.save()

            return HttpResponseRedirect(reverse('auxilioavaliacao:assignment', args=[assignment.id]))
    else:
        form = SubmissionForm()

    context = {
        'form': form,
        'assignment': assignment
    }
    return render(request, 'auxilioavaliacao/new_submission.html', context)

def submission(request, assignment_id, submission_id):

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    context = {
        'assignment': assignment,
        'submission': submission
    }
    return render(request, 'auxilioavaliacao/submission.html', context)

# REST API

class AssignmentViewSet(viewsets.ModelViewSet):
    """ Atividades
    """

    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class AssignmentFieldsViewSet(viewsets.ModelViewSet):
    """ Campos de uma Atividade
    """

    serializer_class = FieldSerializer

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        return Field.objects.filter(assignment__id=assignment_id)

class AssignmentSubmissionsViewSet(viewsets.ModelViewSet):
    """ Entregas de uma Atividade
    """

    serializer_class = SubmissionSerializer

    def get_queryset(self):
        assignment_id = self.kwargs['assignment_id']
        return Submission.objects.filter(assignment__id=assignment_id)

class FieldViewSet(viewsets.ModelViewSet):
    """ Campos
    """

    queryset = Field.objects.all()
    serializer_class = FieldSerializer

class FieldAnswersViewSet(viewsets.ModelViewSet):
    """ Respostas de um Campo
    """

    serializer_class = AnswersSerializer

    def get_queryset(self):
        field_id = self.kwargs['field_id']
        return Answer.objects.filter(field__id=field_id)

class FieldAnswerGroupsViewSet(viewsets.ModelViewSet):
    """ Grupos de um Campo
    """

    serializer_class = AnswerGroupSerializer

    def get_queryset(self):
        field_id = self.kwargs['field_id']
        field = get_object_or_404(Field, pk=field_id)
        return AnswerGroup.objects.filter(field=field)

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

class SubmissionAnswersViewSet(viewsets.ModelViewSet):
    """ Respostas de uma Entrega
    """

    serializer_class = AnswersSerializer

    def get_queryset(self):
        submission_id = self.kwargs['submission_id']
        return Answer.objects.filter(submission__id=submission_id)

class AnswerViewSet(viewsets.ModelViewSet):
    """ Resposta
    """

    queryset = Answer.objects.all()
    serializer_class = AnswersSerializer

class AnswerGroupViewSet(viewsets.ModelViewSet):
    queryset = AnswerGroup.objects.all()
    serializer_class = AnswerGroupSerializer

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
