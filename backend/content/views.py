import json
from django.shortcuts import render

from .models import Content


def main(request):
    content = Content.objects.get(id=1)
    paragraphs = content.content
    paragraphs = json.loads(paragraphs)  # convert content.content into json
    context = {
        "content": content,
        "paragraphs": paragraphs
    }
    return render(request, 'home.html', context)
