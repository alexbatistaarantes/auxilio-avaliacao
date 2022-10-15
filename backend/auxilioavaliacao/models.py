from email.policy import default
from tkinter import CASCADE
from django.db import models

from .utils import crop_image, split_filename_and_extension

def image_directory_path(instance, filename):
    return f"images/{filename}"

class Assignment(models.Model):
    """ Guarda uma Atividade (ex: prova, tarefa)
    """

    title = models.CharField(max_length=255, null=False, blank=True, help_text="O título da atividade")
    template_image = models.ImageField(
        upload_to='templates',
        width_field='width',
        height_field='height',
        null=False,
        blank=False,
        help_text="A imagem que será usada para definir os campos"
    )
    width = models.IntegerField(null=True, blank=True, help_text="A largura da imagem template")
    height = models.IntegerField(null=True, blank=True, help_text="A altura da imagem template")

    def __str__(self):
        return f"({self.id}) {self.title}"

class Field(models.Model):
    """ Guarda um Campo que está presente em uma Atividade (:model:`auxilioavalicao.Assignment`)
    """

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='fields', help_text="A atividade de qual o campo faz parte")
    label = models.CharField(max_length=50, null=False, blank=False, help_text="O nome do campo")
    image = models.ImageField(upload_to='fields', null=True, blank=True, help_text="A imagem do campo")
    x = models.IntegerField(null=False, blank=False, help_text="A coordenada X do ponto esquerdo superior em referência a imagem da entrega")
    y = models.IntegerField(null=False, blank=False, help_text="A coordenada Y do ponto esquerdo superior em referência a imagem da entrega")
    width = models.IntegerField(null=True, blank=True, help_text="A largura da imagem do campo")
    height = models.IntegerField(null=True, blank=True, help_text="A altura da imagem do campo")

    def save(self, *args, **kwargs):
        """ Criando imagem do campo
        """

        # Obtendo imagem do campo a partir da imagem template
        self.image = crop_image(
            self.assignment.template_image,
            (self.x, self.y, self.x + self.width, self.y + self.height)
        )
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.assignment.title} - {self.label}"

class Submission(models.Model):
    """ Guarda uma entrega de uma Atividade (:model:`auxilioavalicao.Assignment`) de um aluno
    """

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions', help_text="A atividade da qual a entrega faz parte")
    studentId = models.CharField(max_length=255, null=False, blank=False, help_text="Um identificador único do aluno dessa entrega")
    image = models.ImageField(
        upload_to='submissions',
        width_field='width',
        height_field='height',
        null=True, blank=True,
        help_text="A imagem da atividade"
    )
    width = models.IntegerField(null=True, blank=True, help_text="A largura da imagem")
    height = models.IntegerField(null=True, blank=True, help_text="A altura da imagem")

    class Meta:
        constraints = [
            models.UniqueConstraint('assignment', 'studentId', name='unique_student_submission_per_assignment')
        ]

    def save(self, *args, **kwargs):
        
        # studentId é definido a partir do nome do arquivo
        self.studentId, _ = split_filename_and_extension(self.image.name)
        super().save(*args, **kwargs)

        self.createAnswer()

    def createAnswer(self):
        """ Cria as respostas (:model:`auxilioavaliacao.Answer`)
        """

        fields = self.assignment.fields.all()
        for field in fields:
            x_percent = field.x / self.assignment.width
            y_percent = field.y / self.assignment.height
            width_percent = field.width / self.assignment.width
            height_percent = field.height / self.assignment.height
            x = int(x_percent * self.width)
            y = int(y_percent * self.height)
            width = int(width_percent * self.width)
            height = int(height_percent * self.height)

            # Se resposta para o campo já existir
            try:
                answer = Answer.objects.get(submission=self, field=field)
                answer.x = x
                answer.y = y
                answer.width = width
                answer.height = height
            except:
                answer = Answer(
                    submission=self,
                    field=field,
                    x=x,
                    y=y,
                    width=width,
                    height=height
                )
            answer.save()

    def __str__(self):
        return f"{self.assignment} - {self.studentId}"

class AnswerGroup(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='groups', help_text="O campo das respostas agrupadas neste grupo")
    name = models.CharField(max_length=30, default='', null=False, blank=False, help_text="Um curto descritor do agrupamento (por exemplo, o conteúdo das respostas)")

    class Meta:
        constraints = [
            models.UniqueConstraint('field', 'name', name='unique_group_name_per_field')
        ]

class Answer(models.Model):
    """ Guarda a imagem da resposta de uma Entrega (:model:`auxilioavalicao.Submission`)
    """

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='answers', help_text="A entrega da qual essa resposta faz parte")
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='answers', help_text="O campo desta resposta")
    image = models.ImageField(
        upload_to='submissionFields',
        null=True, blank=True,
        help_text="A imagem da resposta"
    )
    x = models.IntegerField(null=True, blank=True, help_text="A coordenada X do ponto esquerdo superior em referência a imagem da entrega")
    y = models.IntegerField(null=True, blank=True, help_text="A coordenada Y do ponto esquerdo superior em referência a imagem da entrega")
    width = models.IntegerField(null=True, blank=True, help_text="A largura da imagem da resposta")
    height = models.IntegerField(null=True, blank=True, help_text="A altura da imagem da resposta")
    modified = models.BooleanField(default=False, help_text="Se a região da resposta foi alterada da padrão")
    group = models.ForeignKey(AnswerGroup, on_delete=models.SET_NULL, related_name='answers', null=True, blank=True, help_text="O grupo que esta resposta faz parte")

    class Meta:
        constraints = [
            models.UniqueConstraint('submission', 'field', name='unique_field_per_submission')
        ]

    def save(self, *args, **kwargs):
        """ Obtém imagem da resposta
        """

        # Obtendo imagem do campo a partir da imagem template
        self.submission.image.open()
        self.image = crop_image(
            self.submission.image,
            (self.x, self.y, self.x + self.width, self.y + self.height)
        )

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.submission} - {self.field}"
