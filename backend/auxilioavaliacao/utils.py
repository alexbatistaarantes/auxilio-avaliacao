from PIL import Image
from os.path import basename, splitext
from io import BytesIO
from django.core.files import File
from fpdf import FPDF
from email.mime import base
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email import message_from_bytes
import imaplib
import re

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

def send_grading_email(assignment, submission, grading: bytearray, send_email, password):

    grading = BytesIO(grading)

    msg = MIMEMultipart()
    
    msg['From'] = send_email
    msg['To'] = submission.studentId
    msg['Subject'] = f"Correção {assignment.title}"
    body = f"""Correção da Atividade "{assignment.title}" em anexo."""
    msg.attach(MIMEText(body, 'plain'))

    p = MIMEBase('application', 'pdf')
    p.set_payload(grading.read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f"attachment; filename={assignment.title} - {submission.studentId}.pdf")
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()    
    s.login(send_email, password)
    s.sendmail(send_email, submission.studentId, msg.as_string())
    s.quit()

def get_submissions_email(assignment, recv_email, password):

    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(recv_email, password)

    imap.select(readonly = True)
    _, data = imap.search(None, 'ALL')
    emails_ids = data[0].split()

    for id in emails_ids:
        _, data = imap.fetch(id, '(RFC822)')

        mail = message_from_bytes(data[0][1])

        # Skip if title is not the name of the assignment
        if assignment.title.lower() not in mail['Subject'].lower().strip():
            continue

        student_email = re.search(r".* <(.*)>", mail['From']).group(1)

        for part in mail.walk():
            if part.get_content_type().startswith('image/'):
                file_type = re.search(r".*\.(\w*)$", part.get_filename()).group(1)
                if file_type.lower() in ['png', 'jpg', 'jpeg']:
                    payload = part.get_payload(decode=True)
                    submission = {
                        'email': student_email,
                        'file': [file_type, payload]
                    }
                    yield submission

    imap.close()
    imap.logout()
