#-*- coding:utf-8 -*-


from django.conf import settings

from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from time import localtime, strftime

@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def healthcheck(request):
    return Response(dict(
        status = 'ok',
        app_name = getattr(settings, 'APP_NAME'),
        version = getattr(settings, 'APP_VERSION'),
        update_time = strftime("%a, %d %b %Y %H:%M:%S +0000", localtime())
))
