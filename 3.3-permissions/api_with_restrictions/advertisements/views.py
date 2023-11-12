from django.http import Http404
from django.shortcuts import get_object_or_404
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsFavouriteOwner, IsOwnerOrAdmin
from advertisements.serializers import AdvertisementSerializer, FavouritesSerializer
from advertisements.models import Advertisement, Favourites
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all().prefetch_related('creator')
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return []
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated, IsFavouriteOwner])
    def favourites(self, request):
        queryset = Favourites.objects.all().filter(user=request.user).prefetch_related('advertisement')
        serializer = FavouritesSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'], permission_classes=[IsAuthenticated, IsFavouriteOwner])
    def favourite(self, request, pk=None):
        advertisement = get_object_or_404(Advertisement.objects.all(), pk=pk)
        user = request.user
        if request.method == 'POST':
            data = {
                'user': user, 
                'advertisement': advertisement
            }
            if user == advertisement.creator:
                raise Http404('Нельзя добавить в избранное объявление принадлежащее вам')
            serializer = FavouritesSerializer(FavouritesSerializer().create(data))
            return Response(serializer.data)
        elif request.method == 'DELETE':
            queryset = Favourites.objects.all().filter(user=request.user)
            favourite = get_object_or_404(queryset, advertisement=pk)
            favourite.delete()
            return Response(status=200)
        
