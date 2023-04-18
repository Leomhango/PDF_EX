import json
import PyPDF2
from django.core.files.storage import default_storage

from django.db import models


class Content(models.Model):
    title = models.CharField(max_length=255)
    # image field here
    content = models.JSONField(null=True, blank=True)

    def save(self, *args, **kwargs):
        open_pdf = PyPDF2.PdfReader(self.pdf_file)

        paragraphs = []
        for page_num in range(len(open_pdf.pages)):
            page = open_pdf.pages[page_num]
            extracted_text = page.extract_text()
            paragraphs.extend(extracted_text.split('\n '))

        # Create a dictionary with keys as 'paragraph1', 'paragraph2', '...'.
        # and values as the extracted text
        content = {}
        for i, paragraph in enumerate(paragraphs):
            key = f'paragraph{i+1}'
            content[key] = paragraph.strip()

        # Set the content field to the created dictionary
        self.content = json.dumps(content)

        super(Content, self).save(*args, **kwargs)

    def pdf_file_upload_to(instance, filename):
        return f'pdf_files/{filename}'

    pdf_file = models.FileField(upload_to=pdf_file_upload_to)

    def __str__(self):
        return self.title
