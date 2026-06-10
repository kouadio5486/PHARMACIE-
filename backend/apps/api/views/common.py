"""Constantes et helpers partagés entre les ViewSets."""
from django.db.models import Prefetch, Q

from apps.pharmacies.models import Ville
from apps.stocks.models import Stock


def stocks_disponibles_queryset(ville=None):
    """Stocks en pharmacie active, optionnellement limités à une ville (CI)."""
    qs = Stock.objects.filter(quantite__gt=0, pharmacie__is_active=True).select_related(
        "pharmacie", "pharmacie__ville"
    )
    if ville is not None:
        qs = qs.filter(pharmacie__ville=ville)
    return qs.order_by("prix")


def prefetch_stocks_disponibles(ville=None):
    return Prefetch("stocks", queryset=stocks_disponibles_queryset(ville))


def get_ville_from_request(request):
    """
    ?ville=3 (id) ou ?ville_nom=Yamoussoukro
    """
    ville_id = request.query_params.get("ville")
    ville_nom = request.query_params.get("ville_nom")

    if ville_id:
        try:
            return Ville.objects.get(pk=int(ville_id), is_active=True)
        except (ValueError, Ville.DoesNotExist):
            return None

    if ville_nom:
        nom = ville_nom.strip()
        return Ville.objects.filter(
            Q(nom__iexact=nom) | Q(nom__icontains=nom),
            is_active=True,
        ).first()

    return None
