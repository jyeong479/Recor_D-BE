from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Portfolio, StarEntry
from .serializers import PortfolioSerializer, StarEntrySerializer
from .services import summarize_star_entry


class PortfolioListCreateView(generics.ListCreateAPIView):
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user).prefetch_related('star_entries')


class PortfolioDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)


class StarEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = StarEntrySerializer

    def get_portfolio(self):
        return get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'], user=self.request.user)

    def get_queryset(self):
        return StarEntry.objects.filter(portfolio=self.get_portfolio())

    def perform_create(self, serializer):
        serializer.save(portfolio=self.get_portfolio())


class StarEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StarEntrySerializer

    def get_queryset(self):
        return StarEntry.objects.filter(
            portfolio_id=self.kwargs['portfolio_id'],
            portfolio__user=self.request.user,
        )


class StarEntrySummarizeView(APIView):
    def post(self, request, portfolio_id, pk):
        entry = get_object_or_404(StarEntry, id=pk, portfolio_id=portfolio_id, portfolio__user=request.user)
        entry = summarize_star_entry(entry)
        return Response(StarEntrySerializer(entry).data)
