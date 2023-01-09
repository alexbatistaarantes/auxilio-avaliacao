from email.mime import base
from PIL import Image
from os.path import basename, splitext
from io import BytesIO
from django.core.files import File
from fpdf import FPDF

def crop_image(image, box):
    img = Image.open(image)
    # Obtendo a extensão
    _, extension = split_filename_and_extension(image.name)
    # Corta a imagem
    cropped = img.crop(box)
    # Salvando em um BytesIO
    cropped_IO = BytesIO()
    cropped.save(cropped_IO, format=extension)
    # Salvando em um File do Django
    cropped_file = File(cropped_IO, name=image.name)
    
    return cropped_file

def split_filename_and_extension(filepath):
    splitted = splitext(basename(filepath))
    return splitted[0], splitted[-1][1:]

def get_submission_grading(submission):
    
    report = FPDF()
    report.set_font('helvetica', size=12)
    
    report.add_page()
    report.image(submission.image.path, h=report.eph)

    report.write_html(f"""
        <h1> Atividade: {submission.assignment.title} </h1>
        <h2> Aluno: {submission.studentId} </h2>
        <h2> Nota: {submission.total_points} / {submission.assignment.total_points} </h2>
    """)

    for answer in submission.answers.all():
        report.write_html(f"""
            <h3> {answer.field.label} </h3>
            <h4> {answer.points} / {answer.field.points} </h4>
            <p> {answer.feedback} </p>
        """)
        report.image(answer.image.path, w=report.epw)
        report.write_html("<hr>")

    return report.output()
