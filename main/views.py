import re
from django.shortcuts import render

def convert_html(request):
    converted_html = ''
    
    if request.method == 'POST':
        html_input = request.POST.get('html_input', '')

        # Add {% load static %} at the top if not already present
        if '{% load static %}' not in html_input:
            html_input = '{% load static %}\n' + html_input

        # Convert src="..." for static assets only if NOT a remote link
        html_input = re.sub(
            r'src="(?!https?:\/\/|\/\/)([^"]+)"',
            lambda m: f'src="{{% static \'{m.group(1)}\' %}}"',
            html_input
        )
        html_input = re.sub(
            r"src='(?!https?:\/\/|\/\/)([^']+)'",
            lambda m: f"src='{{% static \'{m.group(1)}\' %}}'",
            html_input
        )


        # Convert href for static asset files (css, js, images)
       # NEW: Only convert local paths (not full URLs)
        html_input = re.sub(
            r'href="(?!https?:\/\/|\/\/)([^"]+\.(css|js|png|jpg|jpeg|svg))"',
            lambda m: f'href="{{% static \'{m.group(1)}\' %}}"',
            html_input
        )
        html_input = re.sub(
            r"href='(?!https?:\/\/|\/\/)([^']+\.(css|js|png|jpg|jpeg|svg))'",
            lambda m: f"href='{{% static \'{m.group(1)}\' %}}'",
            html_input
        )


        # Convert href="something.html" to {% url 'something' %}
        html_input = re.sub(
            r'href="([^"]+)\.html"',
            lambda m: f'href="{{% url \'{m.group(1)}\' %}}"',
            html_input
        )
        html_input = re.sub(
            r"href='([^']+)\.html'",
            lambda m: f"href='{{% url \'{m.group(1)}\' %}}'",
            html_input
        )

        # Convert href="/something/" to {% url 'something' %}
        html_input = re.sub(
            r'href="/([^"/]+)/"',
            lambda m: f'href="{{% url \'{m.group(1)}\' %}}"',
            html_input
        )
        html_input = re.sub(
            r"href='/([^'/]+)/'",
            lambda m: f"href='{{% url \'{m.group(1)}\' %}}'",
            html_input
        )


        converted_html = html_input

    return render(request, 'index.html', {'converted_html': converted_html})
