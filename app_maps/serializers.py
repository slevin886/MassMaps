from rest_framework import serializers
from .models import Origins, Commute


class CommutePostSerializer(serializers.Serializer):
    origin_name = serializers.CharField(max_length=50)
    mode = serializers.CharField(max_length=20)
    date = serializers.DateTimeField()
    distance = serializers.IntegerField()
    duration = serializers.IntegerField()
    in_traffic = serializers.IntegerField(allow_null=True)


class CommuteSerializer(serializers.ModelSerializer):
    origin_name = serializers.CharField(source='origin.name')

    class Meta:
        model = Commute
        fields = ('origin_name', 'date', 'distance', 'duration', 'in_traffic',
                  'mode',)
    #
    # def create(self, validated_data):
    #     origin_name = validated_data.pop('origin_name')
    #     origin = Origins.objects.get(origin_name)
    #     return Commute.objects.create(**validated_data, origin=origin)
    #
    # def update(self, instance, validated_data):
    #     raise Exception('Not implemented')


# class RequestSerializer(serializers.Serializer):
#     pass


