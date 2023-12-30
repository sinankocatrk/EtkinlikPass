from django.shortcuts import render
from advert.models import Advert

def index(request):

    print(request.user.id)
    all_adverts = Advert.objects.all()

    undeleted_adverts_count = all_adverts.filter(is_deleted=False).count()

    keyword = request.GET.get("keyword")


    if keyword :
        keyword = keyword.lower()
        filtered_adverts = Advert.objects.filter(event__title__icontains=keyword)
        undeleted_filtered_adverts_count = filtered_adverts.filter(is_deleted=False).count()
        filtered_adverts_context = {
            "all_adverts": filtered_adverts,
            "undeleted_adverts_count": undeleted_filtered_adverts_count,
            "keyword": keyword,
        }
        return render(request,"index.html",context=filtered_adverts_context)

    context = {
        "all_adverts": all_adverts,
        "undeleted_adverts_count": undeleted_adverts_count,
        "keyword": None
    }

    return render(request, "index.html", context)
