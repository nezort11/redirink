from django.urls import reverse
from rest_framework import serializers

from redirink.links.models import Link


class LinkSerializer(serializers.ModelSerializer):
    """
    Serializer to dict for link.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    from_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ["pk", "from_url", "to_url", "create_time", "user"]
        extra_kwargs = {
            "pk": {"read_only": True},
            "create_time": {"read_only": True},
        }

    def validate(self, data: dict) -> dict:
        return data

    def get_from_url(self, obj):
        request = self.context["request"]
        redirect_path = reverse("links:redirect", kwargs={"pk": obj.pk})
        return f"{request.scheme}://{request.get_host()}{redirect_path}"
