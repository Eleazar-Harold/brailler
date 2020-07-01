import random

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from brl.app_conv import BrCnvx
from brl.forms import B2TForm, T2BForm


def ttob_page(request):
    if request.method == "GET":
        form = T2BForm()
        context = {"form": form, "title": "Braille Converter"}
        return render(request, "pages/ttob.html", context)
    elif request.method == "POST":
        form = T2BForm(request.POST)
        if form.is_valid():
            # Get values of each field
            message = form.cleaned_data["message"]
            msg_entered = message.lower()
            br = BrCnvx(val=msg_entered)  # Braille(msg_entered)
            result = br.user_text()  # br.to_braille()
            request.session["text_to_braille"] = result
            context = {"form": form, "title": "Braille Converter", "result": result}
            return render(request, "pages/ttob.html", context)


def btot_page(request):
    if request.method == "GET":
        form = B2TForm()
        context = {"form": form, "title": "Text Converter"}
        return render(request, "pages/btot.html", context)
    elif request.method == "POST":
        form = B2TForm(request.POST)
        if form.is_valid():
            # Get values of each field
            message = form.cleaned_data["message"]
            msg_entered = message.lower()
            br = BrCnvx(val=msg_entered)  # Braille(msg_entered)
            result = br.user_braille()  # br.to_ascii()
            request.session["braille_to_text"] = result
            context = {"form": form, "title": "Text Converter", "result": result}
            return render(request, "pages/btot.html", context)


def t2b_print(request):
    response = HttpResponse(content_type="application/pdf")
    doc_name = "t-to-b-{}.pdf".format(str(random.randint(100010001, 999999999)))

    if request.session["text_to_braille"]:
        pdf_printer(doc_name=doc_name, input=request.session["text_to_braille"])
        fs = FileSystemStorage("/tmp")
        filename = doc_name
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response = HttpResponse(pdf, content_type="application/pdf")
                response["Content-Disposition"] = "attachment; filename={}".format(
                    doc_name
                )
                try:
                    del request.session["text_to_braille"]
                except KeyError:
                    pass
        return response
    else:
        return HttpResponseNotFound("The requested pdf was not found in our server.")


def b2t_print(request):
    response = HttpResponse(content_type="application/pdf")
    doc_name = "b-to-t-{}.pdf".format(str(random.randint(100010001, 999999999)))

    if request.session["braille_to_text"]:
        pdf_printer(doc_name=doc_name, input=request.session["braille_to_text"])
        fs = FileSystemStorage("/tmp")
        filename = doc_name
        if fs.exists(filename):
            with fs.open(filename) as pdf:
                response = HttpResponse(pdf, content_type="application/pdf")
                response["Content-Disposition"] = "attachment; filename={}".format(
                    doc_name
                )
            try:
                del request.session["braille_to_text"]
            except KeyError:
                pass
        return response
    else:
        return HttpResponseNotFound("The requested pdf was not found in our server.")


def pdf_printer(doc_name=None, input=None):
    doc = SimpleDocTemplate(
        "/tmp/{}".format(doc_name),
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    Story = []
    Story.append(Spacer(1, 12))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Justify", alignment=TA_JUSTIFY))
    p_text = "<font size=12>%s</font>" % input
    Story.append(Paragraph(p_text, styles["Justify"]))
    Story.append(Spacer(1, 12))
    return doc.build(Story)
