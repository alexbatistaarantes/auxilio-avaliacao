from tkinter import CASCADE
from django.db import models

from .utils import crop_image

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

class Field(models.Model):
    """ Guarda um Campo que está presente em uma Atividade (:model:`auxilioavalicao.Assignment`)
    """

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, help_text="A atividade de qual o campo faz parte")
    label = models.CharField(max_length=50, null=False, blank=False, help_text="O nome do campo")
    image = models.ImageField(upload_to='fields', width_field='width', height_field='height', null=True, blank=True, help_text="A imagem do campo")
    width = models.IntegerField(null=True, blank=True, help_text="A largura da imagem do campo")
    height = models.IntegerField(null=True, blank=True, help_text="A altura da imagem do campo")
    # MELHORAR: salvar apenas o percentual
    # Usar Annotorious (https://recogito.github.io/annotorious/) que tem como salvar o percentual
    x1 = models.IntegerField(null=False, blank=False, help_text="A coordenada X do ponto esquerdo superior em referência a imagem da entrega")
    y1 = models.IntegerField(null=False, blank=False, help_text="A coordenada Y do ponto esquerdo superior em referência a imagem da entrega")
    x2 = models.IntegerField(null=False, blank=False, help_text="A coordenada X do ponto direito inferior em referência a imagem da entrega")
    y2 = models.IntegerField(null=False, blank=False, help_text="A coordenada Y do ponto direito inferior em referência a imagem da entrega")
    pctX1 = models.FloatField(null=True, blank=True, help_text="O percentual do ponto esquerdo superior em relação a largura da imagem template")
    pctY1 = models.FloatField(null=True, blank=True, help_text="O percentual do ponto esquerdo superior em relação a altura da imagem template")
    pctX2 = models.FloatField(null=True, blank=True, help_text="O percentual do ponto direito inferior em relação a largura da imagem template")
    pctY2 = models.FloatField(null=True, blank=True, help_text="O percentual do ponto direito inferior em relação a altura da imagem template")

    def save(self, *args, **kwargs):
        """ Obtém imagem do campo e os percentuais dos pontos
        """

        # Obtendo imagem do campo a partir da imagem template
        self.image = crop_image(self.assignment.template_image, (self.x1, self.y1, self.x2, self.y2))
        
        # Obtendo percentuais
        template_width = self.assignment.width
        template_height = self.assignment.height
        self.pctX1 = self.x1 / template_width
        self.pctY1 = self.y1 / template_height
        self.pctX2 = self.x2 / template_width
        self.pctY2 = self.y2 / template_height
        
        super().save(*args, **kwargs)

class Submission(models.Model):
    """ Guarda uma entrega de uma Atividade (:model:`auxilioavalicao.Assignment`) de um aluno
    """

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, help_text="A atividade da qual a entrega faz parte")
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
        """ Automaticamente obtém as respostas (:model:`auxilioavaliacao.Answer`) a partir dos campos (:model:`auxilioavaliacao.Field`) da atividade (:model:`auxilioavaliacao.Assignment`)
        """

        super().save(*args, **kwargs)

        fields = self.assignment.field_set.all()
        for field in fields:
            x1 = int(self.width * field.pctX1)
            y1 = int(self.height * field.pctY1)
            x2 = int(self.width * field.pctX2)
            y2 = int(self.height * field.pctY2)

            answer = Answer(
                submission=self,
                field=field,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2
            )
            answer.save()

        super().save(*args, **kwargs)

    def save_answer(self, field):
        pass

class Answer(models.Model):
    """ Guarda a imagem da resposta de uma Entrega (:model:`auxilioavalicao.Submission`)
    """

    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, help_text="A entrega da qual essa resposta faz parte")
    field = models.ForeignKey(Field, on_delete=models.CASCADE, help_text="O campo desta resposta")
    image = models.ImageField(
        upload_to='submissionFields',
        null=True, blank=True,
        help_text="A imagem da resposta"
    )
    x1 = models.IntegerField(null=True, blank=True, help_text="A coordenada X do ponto esquerdo superior em referência a imagem da entrega")
    y1 = models.IntegerField(null=True, blank=True, help_text="A coordenada Y do ponto esquerdo superior em referência a imagem da entrega")
    x2 = models.IntegerField(null=True, blank=True, help_text="A coordenada X do ponto direito inferior em referência a imagem da entrega")
    y2 = models.IntegerField(null=True, blank=True, help_text="A coordenada Y do ponto direito inferior em referência a imagem da entrega")

    class Meta:
        constraints = [
            models.UniqueConstraint('submission', 'field', name='unique_field_per_submission')
        ]

    def save(self, *args, **kwargs):
        """ Obtém imagem da resposta
        """

        # Obtendo imagem do campo a partir da imagem template
        self.submission.image.open()
        self.image = crop_image(self.submission.image, (self.x1, self.y1, self.x2, self.y2))

        super().save(*args, **kwargs)
