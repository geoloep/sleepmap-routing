from rest_framework.views import APIView
from rest_framework.response import Response

from .router import RouteHelper

# Create your views here.
class Route(APIView):
    def get(self, request):
        helper = RouteHelper()

        in_start = (5.098, 52.091)
        in_end = (5.103, 52.094)

        start = helper.get_node(*in_start)
        end = helper.get_node(*in_end)

        print(start, end)

        route = helper.get_route(start, end)

        gj = helper.route_to_geojson(route)

        # r = helper.test()
        # t = helper.get_node(5.098, 52.091)
        
        return Response({'route': {
            'start': start,
            'end': end,
            'route': route,
            'geojson': gj,
        }})