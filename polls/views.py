from rest_framework import viewsets

from .models import Poll, Question, Choice, Vote, PollUser
from .serializers import (
    PollListSerializer,
    PollDetailSerializer,
    QuestionListSerializer,
    QuestionDetailSerializer,
    ChoiceSerializer,
    VoteSerializer,
)


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PollListSerializer
        return PollDetailSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return QuestionListSerializer
        return QuestionDetailSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)
        user = PollUser.objects.create()
        return serializer.save(user=user)

