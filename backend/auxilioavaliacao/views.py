from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import base64
from django.core.files.base import ContentFile
from rest_framework import viewsets

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
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswersSerializer
