from django.shortcuts import render, redirect
from .models import VotingForm, Question, Option
from .forms import CreateVotingForm, QuestionForm, OptionForm
import random, string

def create_a_form(request):
    code = None
    questions = [None] * 3
    options = [[None] * 4 for _ in range(3)]

    if request.method == 'POST':
        # Retrieve questions and options from the form submission
        for i in range(3):
            questions[i] = request.POST.get(f'question_{i}')
            options[i] = [
                request.POST.get(f'option1_{i}'),
                request.POST.get(f'option2_{i}'),
                request.POST.get(f'option3_{i}'),
                request.POST.get(f'option4_{i}'),
            ]

        # Generate a random 6-digit alphanumeric code
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))

        # Save the voting form to the database
        voting_form = VotingForm.objects.create(code=code)

        # Save questions and options to the database
        for question_text in questions:
            if question_text:  # Only save non-empty questions
                question = Question.objects.create(form=voting_form, text=question_text)
                for option_text in options[questions.index(question_text)]:
                    if option_text:  # Only save non-empty options
                        Option.objects.create(question=question, text=option_text)

        # After saving, redirect to the same page to show the generated code
        return render(request, 'create_a_form.html', {
            'code': voting_form.code,  # Pass the generated code to the template
            'questions': questions,
            'options': options,
        })

    return render(request, 'create_a_form.html', {
        'code': code,  # Initially, code is None when not submitted
        'questions': questions,
        'options': options,
    })

def vote_on_a_form(request):
    if request.method == 'POST':
        code = request.POST.get('code', None)

        # If there is an option selected (indicating a vote), update the vote count
        option_selected = request.POST.get('option_id')
        if option_selected:
            try:
                # Retrieve the selected option and increment its vote count
                option = Option.objects.get(id=option_selected)
                option.votes += 1
                option.save()
                message = "Your vote has been recorded!"  # Message to confirm vote success
            except Option.DoesNotExist:
                message = "Option not found. Please try again."

            # Retrieve the form and questions to stay on the same page
            voting_form = option.question.form
            questions = Question.objects.filter(form=voting_form)
            return render(request, 'vote_on_a_form.html', {'questions': questions, 'code': code, 'message': message})

        # If only the code was submitted, retrieve the form questions
        try:
            voting_form = VotingForm.objects.get(code=code)
            questions = Question.objects.filter(form=voting_form)
            return render(request, 'vote_on_a_form.html', {'questions': questions, 'code': code})
        except VotingForm.DoesNotExist:
            return render(request, 'vote_on_a_form.html', {'error': 'Invalid code'})

    return render(request, 'vote_on_a_form.html')


def result(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            voting_form = VotingForm.objects.get(code=code)
            questions = Question.objects.filter(form=voting_form)
            return render(request, 'result.html', {'questions': questions})
        except VotingForm.DoesNotExist:
            return render(request, 'result.html', {'error': 'Invalid code'})
    return render(request, 'result.html')
