import json
from django.db import connection
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import View
from arches.app.models import models
from arches.app.utils.response import JSONResponse
from arches.app.views.search import search_results

class MVT_Parcels(View):
    def get(self, request, zoom, x, y):
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT ST_AsMVT(tile, 'parcels', 4096, 'geom', 'id')
                    FROM (SELECT row_number() over () as id,
                            ownparcelid as displayname,
                            ST_AsMVTGeom(
                                ST_CurveToLine(geom),
                                TileBBox(%s, %s, %s, 4326)) AS geom,
                            CONCAT('/geojson-parcel/', ownparcelid) AS geojson
                        FROM parcels) AS tile""",
                    [zoom, x, y])
            tile = bytes(cursor.fetchone()[0])
            if not len(tile):
                raise Http404()
        return HttpResponse(tile, content_type="application/x-protobuf")

class Geojson_Parcels(View):
    def get(self, request, selectedApn):
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT ST_AsGeoJSON(geom)::json
                    FROM parcels
                    WHERE apn = %s""",
                    [selectedApn])
            feature = cursor.fetchone()[0]
            if not len(feature):
                raise Http404()
        response = JSONResponse({"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": feature, "properties": {}}]})
        return response