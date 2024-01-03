from django.shortcuts import render
from advert.models import Advert
from django.db.models import Q

def index(request):
    keyword = request.GET.get("keyword", "").strip()

    if keyword:
        adverts = Advert.objects.filter(
            Q(event__title__icontains=keyword) |
            Q(event__description__icontains=keyword) |
            Q(event__city__icontains=keyword) |
            Q(event__location__icontains=keyword),
            is_deleted=False
        )
    else:
        adverts = Advert.objects.filter(is_deleted=False)

    adverts_count = adverts.count()

    context = {
        "all_adverts": adverts,
        "undeleted_adverts_count": adverts_count,
        "keyword": keyword if keyword else "",
    }

    return render(request, "index.html", context=context)
