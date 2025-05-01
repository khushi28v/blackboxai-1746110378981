from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Property
from .forms import ContactForm

def home(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    properties = Property.objects.all().order_by('-id')

    if query:
        properties = properties.filter(
            Q(location__icontains=query) |
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)

    paginator = Paginator(properties, 6)  # 6 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'properties': page_obj,
        'query': query or '',
        'min_price': min_price or '',
        'max_price': max_price or '',
        'page_obj': page_obj,
    }
    return render(request, 'listings/home.html', context)

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    google_maps_api_key = 'YOUR_GOOGLE_MAPS_API_KEY'  # Replace with your actual API key
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Here you can handle the form data, e.g., send email or save inquiry
            return redirect('listings:home')
    else:
        form = ContactForm()
    return render(request, 'listings/property_detail.html', {'property': property, 'form': form, 'google_maps_api_key': google_maps_api_key})
