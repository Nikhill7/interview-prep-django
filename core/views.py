# interview_prep_django/core/views.py

import os
from django.shortcuts import render
import google.generativeai as genai
from .forms import QuestionGenerationForm  # Import your new form


def index(request):
    form = QuestionGenerationForm()
    return render(request, 'index.html', {'form': form})


def generate_questions_view(request):
    generated_questions = []
    error_message = None

    if request.method == 'POST':
        form = QuestionGenerationForm(request.POST)
        if form.is_valid():
            job_role = form.cleaned_data['job_role']
            question_type = form.cleaned_data['question_type']
            num_questions = form.cleaned_data['num_questions']

            try:
                gemini_api_key = os.environ.get('GEMINI_API_KEY')
                if not gemini_api_key:
                    raise ValueError("GEMINI_API_KEY not set in environment variables.")

                genai.configure(api_key=gemini_api_key)

                # --- CHANGE THIS LINE ---
                model = genai.GenerativeModel('gemini-pro-latest')  # Use the newly identified 'gemini-pro-latest' model
                # --- END CHANGE ---

                prompt_template = f"""
                Generate {num_questions} {question_type} interview questions for a {job_role} role.
                Focus on questions that assess practical skills and problem-solving relevant to the role.
                Format them as a numbered list.
                """

                response = model.generate_content(prompt_template)
                raw_questions = response.text

                questions_lines = raw_questions.split('\n')
                for line in questions_lines:
                    if line.strip() and line.strip()[0].isdigit() and '.' in line.strip():
                        clean_question = line.strip().split('.', 1)[1].strip()
                        if clean_question:
                            generated_questions.append(clean_question)

                if not generated_questions and raw_questions:
                    generated_questions = [raw_questions.strip()]
                elif not generated_questions:
                    error_message = "Gemini generated an unexpected response. Please try again or refine your request."

            except Exception as e:
                print(f"Error generating questions with Gemini: {e}")
                error_message = f"Failed to generate questions. Error: {e}"
        else:
            pass  # Form is not valid, errors will be displayed in the template

    else:
        form = QuestionGenerationForm()

    return render(request, 'index.html', {
        'form': form,
        'generated_questions': generated_questions,
        'error_message': error_message
    })