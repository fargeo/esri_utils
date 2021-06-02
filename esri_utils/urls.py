from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from esri_utils.views.overlays import MVT_Parcels, Geojson_Parcels


urlpatterns = [
    url(r'^', include('arches.urls')),
    url(
        r"^mvt-parcels/(?P<zoom>[0-9]+|\{z\})/(?P<x>[0-9]+|\{x\})/(?P<y>[0-9]+|\{y\}).pbf$",
        MVT_Parcels.as_view(), name="mvt-parcels",
    ),
    url(r"^geojson-parcel/(?P<selectedApn>.*)$", Geojson_Parcels.as_view(), name="geojson_parcel"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
