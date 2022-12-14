from rest_framework import serializers

from .models import Poll, Question, Choice, Answer, Vote, PollUser
from .fields import ObjectIDField


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'text', )
        read_only_fields = ('id', )


class QuestionListSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, write_only=True)

    class Meta:
        model = Question
        fields = ('id', 'poll', 'text', 'type', 'choices', )
        read_only_fields = ('id', )

    def create_choices(self, question, choices):
        Choice.objects.bulk_create([Choice(question=question, **d) for d in choices])

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        self.create_choices(question, choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.choice_set.all().delete()
        self.create_choices(instance, choices)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionDetailSerializer(QuestionListSerializer):
    choices = ChoiceSerializer(many=True)


class PollListSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_date', 'end_date', 'description', 'questions')
        read_only_fields = ('id', )

    def create(self, validated_data):
        questions = validated_data.pop('questions', [])
        poll = Poll.objects.create(**validated_data)
        Question.objects.bulk_create([Question(poll=poll, **d) for d in questions])
        return poll


class PollDetailSerializer(PollListSerializer):
    questions = QuestionListSerializer(many=True)


class AnswerSerializer(serializers.ModelSerializer):
    choice = ChoiceSerializer(read_only=True)
    choice_id = ObjectIDField(queryset=Choice.objects.all(), write_only=True)

    question = QuestionDetailSerializer(read_only=True)
    question_id = ObjectIDField(queryset=Question.objects.all(), write_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'question', 'choice_id', 'choice', 'value',)
        read_only_fields = ('id',)


class VoteSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    poll = PollListSerializer(read_only=True)
    poll_id = ObjectIDField(queryset=Poll.objects.all(), write_only=True)

    class Meta:
        model = Vote
        fields = ('id', 'poll_id', 'poll', 'user', 'answers',)
        read_only_fields = ('id', 'user',)

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        vote = Vote.objects.create(**validated_data)
        Answer.objects.bulk_create([Answer(vote=vote, **d) for d in answers])
        return vote
