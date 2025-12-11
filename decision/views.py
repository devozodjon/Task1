from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .models import Attribute, AttributeValue, Rule, Applicant

# Bosh sahifa
def index(request):
    return render(request, 'index.html')

# User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=401)
    return HttpResponseForbidden()

# User logout
def user_logout(request):
    logout(request)
    return redirect('tree:index')

# API: statistikani qaytarish
@login_required
def api_stats(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    data = {
        'applicants': Applicant.objects.count(),
        'rules': Rule.objects.count(),
        'attributes': Attribute.objects.count(),
        'values': AttributeValue.objects.count()
    }
    return JsonResponse(data)

# API: atributlar
def api_attributes(request):
    data = list(Attribute.objects.values())
    return JsonResponse(data, safe=False)

# API: atribut qiymatlari
def api_attribute_values(request):
    data = list(AttributeValue.objects.values())
    return JsonResponse(data, safe=False)

# API: qoidalar
def api_rules(request):
    rules = Rule.objects.all()
    data = []
    for r in rules:
        data.append({
            'id': r.id,
            'shartlar': r.shartlar,  # bu field JSON bo‘lishi kerak
            'natija': r.natija
        })
    return JsonResponse(data, safe=False)

# API: arizalar
def api_applicants(request):
    data = list(Applicant.objects.values())
    return JsonResponse(data, safe=False)

# API: o'chirish (CRUD)
@login_required
def api_attribute_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    Attribute.objects.filter(pk=pk).delete()
    return JsonResponse({'deleted': True})

@login_required
def api_attribute_value_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    AttributeValue.objects.filter(pk=pk).delete()
    return JsonResponse({'deleted': True})

@login_required
def api_rule_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    Rule.objects.filter(pk=pk).delete()
    return JsonResponse({'deleted': True})

@login_required
def api_applicant_delete(request, pk):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    Applicant.objects.filter(pk=pk).delete()
    return JsonResponse({'deleted': True})

# Ariza saqlash
def save_application(request):
    if request.method == 'POST':
        applicant = Applicant()
        # barcha atributlarni tekshirib saqlash
        for attr in Attribute.objects.all():
            value = request.POST.get(attr.nomi)
            if value:
                setattr(applicant, attr.nomi.lower().replace(' ', '_'), value)
        applicant.natija = request.POST.get('natija', 'Noma\'lum')
        applicant.save()
        return JsonResponse({'success': True})
    return HttpResponseForbidden()
