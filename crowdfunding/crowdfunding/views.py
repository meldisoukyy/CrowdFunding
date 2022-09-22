from django.shortcuts import render


def custom_page_not_found_view(request, exception):
    return render(request, "errors/404.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})