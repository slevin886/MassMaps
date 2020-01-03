from django.shortcuts import render
from django.db.models import Sum, Avg, CharField
from django.db.models.functions import TruncDate, Cast
from .models import Commute, Origins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CommuteSerializer, CommutePostSerializer


class CommuteList(APIView):
    """
    Get all commute time/distance or create new commute.
    """

    def get(self, request, format=None):
        commutes = Commute.objects.all()[:5]
        serializer = CommuteSerializer(commutes, many=True)
        return Response(serializer.data)
        # return Response(serializers.serialize('json', commutes))

    def post(self, request, format=None):
        serializer = CommutePostSerializer(data=request.data)
        if serializer.is_valid():
            print('data valid created')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request):
    # TODO: only works for driving for now
    avg_commutes = Commute.objects.filter(mode='driving').values(
        'origin__name',
        'origin__latitude',
        'origin__longitude',
    ).annotate(
        average_time_dist=Avg('in_traffic') / Avg('distance'),
        average_time=Avg('in_traffic'),
        average_traffic=Avg('in_traffic') - Avg('duration')
    ).order_by(
        'average_time_dist'
    ).all()

    morning_commutes = Commute.objects.filter(mode='driving', date__hour__lt=12).values(
        time=Cast(TruncDate('date'), CharField())
    ).annotate(
        avg_time=Avg('in_traffic')
    ).values('time', 'avg_time')

    evening_commutes = Commute.objects.filter(
        mode='driving', date__hour__gt=12
    ).values('date__date').order_by('date__date').annotate(avg_time=Avg('in_traffic')).annotate(
        time=Cast(TruncDate('date'), CharField())).values('time', 'avg_time')

    return render(request, 'app_maps/home.html', {
        'avg_commutes': list(avg_commutes),
        'evening_commutes': list(evening_commutes),
        'morning_commutes': list(morning_commutes),
    })
