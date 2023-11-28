from .forms import SearchForm


def search_form(request):
    frm = SearchForm(request.GET)
    query = ""
    if "query" in request.GET and frm.is_valid:
        query = request.GET["query"]
        # query = frm.cleaned_data
    return {"search_form": frm, "query": query}
