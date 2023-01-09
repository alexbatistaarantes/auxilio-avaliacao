from django.template import Context, Template
t = Template("My name is {{ my_name }}.")
c = Context({"my_name": "Adrian"})
output = t.render(c)

from auxilioavaliacao.models import *

from fpdf import FPDF

def get_grading_report(submission):
    
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

    report.output(f"reports/{submission.studentId}_grading_report.pdf")

assignment = Assignment.objects.all()[0]
for submission in assignment.submissions.all():
    get_grading_report(submission)
