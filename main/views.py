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

        card_pattern = re.findall(
            r'(<div class="card.*?</div>\s*</div>)', html_input, re.DOTALL)

        # Check for repeated cards
        card_counts = {}
        for card in card_pattern:
            card_counts[card] = card_counts.get(card, 0) + 1

        # If any card is repeated > 1, convert to {% for %}
        for card, count in card_counts.items():
            if count > 1:
                # Replace values in the card to generic placeholders
                card_for_loop = re.sub(r'src="{% static \'([^"]+)\' %}"', r'src="{{ item.image }}"', card)
                card_for_loop = re.sub(r'<p id="header">([^<]+)</p>', r'<p id="header">{{ item.title }}</p>', card_for_loop)
                card_for_loop = re.sub(r'<p>\s*(.*?)\s*</p>', r'<p>{{ item.description }}</p>', card_for_loop, count=1)

                loop_code = (
                    '{% for item in items %}\n' +
                    card_for_loop +
                    '\n{% endfor %}'
                )

                html_input = html_input.replace(card, '', count - 1)  # remove duplicates
                html_input = html_input.replace(card, loop_code, 1)  # replace the first one with loop


        converted_html = html_input

    return render(request, 'index.html', {'converted_html': converted_html})
