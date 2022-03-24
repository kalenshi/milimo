from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.serializers import HiveConfigSerializer

REQUIRED = ["bucket", "access_key", "secret_key", "endpoint"]


class S3ConfigView(APIView):
    """
    CLass for interacting with the S3 config file
    """
    serializer_class = HiveConfigSerializer

    def get(self, request, format=None):
        """
        Endpoint to view the current config file
        :param request:
        :param format:
        :return:
        """
        return Response({"message": "coming soon"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "bucket": openapi.Schema(type=openapi.TYPE_STRING),
                "access_key": openapi.Schema(type=openapi.TYPE_STRING),
                "secret_key": openapi.Schema(type=openapi.TYPE_STRING),
                "endpoint": openapi.Schema(type=openapi.TYPE_STRING),
                "path_style_access": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN,
                    default=False
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="`About this config`"
                ),
            },
            required=REQUIRED
        )
    )
    def post(self, request, format=None):
        """
        Will be used to append to the current XML document
        :param request:
        :param format:
        :return:
        """
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
