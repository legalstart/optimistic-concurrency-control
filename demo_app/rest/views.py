from hashlib import md5
from rest_framework.generics import RetrieveAPIView, UpdateAPIView

from .serializers import DocumentSerializer
from .optimistic_concurrency import optimistic_concurrency_control
from ..models import Document


def _compute_etag(self):
    return md5(self.get_object().text.encode('utf-8')).hexdigest()

@optimistic_concurrency_control(_compute_etag)
class DocumentView(RetrieveAPIView, UpdateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
