from rest_framework.views import APIView
from rest_framework.response import Response

from .router import RouteHelper

# Create your views here.
class Route(APIView):
    def post(self, request):
        if ('start' in request.data and 'end' in request.data):
            try:
                helper = RouteHelper()
                
                start = helper.get_node(*request.data['start']['geometry']['coordinates'])
                end = helper.get_node(*request.data['end']['geometry']['coordinates'])

                route = helper.get_route(start, end)

                gj = helper.route_to_geojson(route)

                return Response({'route': {
                    'start': start,
                    'end': end,
                    'geojson': gj,
                }})
                
            except KeyError as e:
                print (e)
                return Response({"error": "An error occurred while trying to proces your input"}, 500)
        else:
            return Response({"error": "start and end need to be specified"}, 400)
