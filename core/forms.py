# interview_prep_django/core/forms.py

from django import forms

class QuestionGenerationForm(forms.Form):
    job_role = forms.CharField(
        label='Job Role',
        max_length=100,
        help_text='e.g., Software Engineer, Marketing Manager',
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter Job Role'})
    )
    question_type = forms.ChoiceField(
        label='Question Type',
        choices=[
            ('behavioral', 'Behavioral'),
            ('technical', 'Technical'),
            ('situational', 'Situational'),
            ('brain-teaser', 'Brain Teaser'),
            ('general', 'General / Mixed') # Added for broader options
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    num_questions = forms.IntegerField(
        label='Number of Questions',
        min_value=1,
        max_value=10,
        initial=3,
        help_text='How many questions to generate (1-10)',
        widget=forms.NumberInput(attrs={'class': 'form-input'})
    )