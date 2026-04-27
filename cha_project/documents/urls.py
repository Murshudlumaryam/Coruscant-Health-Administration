from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('my/', views.my_documents, name='my_documents'),
    path('download/<int:doc_id>/', views.download_document, name='download_document'),
]
