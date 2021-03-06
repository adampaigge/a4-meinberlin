from rest_framework import serializers

from . import models
from . import validators


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = models.Choice
        fields = ('id', 'label')


class QuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'label', 'choices')


class PollSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = models.Poll
        fields = ('id', 'questions')

    def update(self, instance, data):
        # Delete removed questions from the database
        instance.questions.exclude(
            id__in=[question['id']
                    for question in data['questions']
                    if 'id' in question
                    ]).delete()

        # Update (or create) the questions
        for weight, question in enumerate(data['questions']):
            question_id = question.get('id')
            question_instance, _ = models.Question.objects.update_or_create(
                id=question_id,
                defaults={
                    'poll': instance,
                    'label': question['label'],
                    'weight': weight
                })

            self._update_choices(question, question_instance)

        return instance

    def _update_choices(self, question, question_instance):
        # Delete removed choices from the database
        choice_ids = [choice['id']
                      for choice in question['choices']
                      if 'id' in choice]
        question_instance.choices.exclude(id__in=choice_ids).delete()

        # Update (or create) this questions choices
        for choice in question['choices']:
            choice_id = choice.get('id')
            choice_instance, _ = models.Choice.objects.update_or_create(
                id=choice_id,
                defaults={
                    'question': question_instance,
                    'label': choice['label']
                }
            )


class VoteSerializer(serializers.ModelSerializer):

    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = models.Vote
        fields = ['choice', 'creator']

    def validate(self, data):
        pk = self.instance.pk if self.instance else None
        validators.single_vote_per_user(data['creator'], data['choice'], pk)

        question_pk = self._context.get('question_pk', None)
        if question_pk:
            validators.choice_belongs_to_question(data['choice'], question_pk)

        return data
