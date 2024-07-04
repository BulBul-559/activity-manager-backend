from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from django.utils import timezone

from ..models import Youtholer
from ..models import Machine
from ..models import Activity

from ..serializers import MachineSerializer
from ..serializers import ActivitySerializer

from intervaltree import IntervalTree
from datetime import datetime
