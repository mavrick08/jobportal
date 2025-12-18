from django import forms
from .models import Job
import datetime
class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','description','company','location','job_type','deadline','salary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','min':datetime.date.today().strftime('%Y-%m-%d')}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            }
        
        def __init__(self,*args,**kwargs):
            super(JobPostForm,self).__init__(*args,**kwargs)
            # self.fields['deadline'].widget.attrs['min'] = datetime.date.today().isoformat()
            for field in self.fields.values():
                field.widget.attrs.update({'class':'form-control'})
        
        # def clean_deadline(self):
        #     deadline = self.cleaned_data.get('deadline')
        #     if deadline and deadline < datetime.date.today():
        #         raise forms.ValidationError("Deadline cannot be in the past")
        #     return deadline
