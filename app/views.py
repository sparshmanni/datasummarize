from django.shortcuts import render
import pandas as pd

from .forms import uploadfileform

from django.core.mail import send_mail

from django.http import HttpResponseBadRequest


def sumry(f):
    data= pd.read_excel(f)
    summary=data.groupby(['Cust State','DPD']).size().reset_index(name='Count')
    state_summary = summary.groupby('Cust State').agg({'Count': 'sum', 'DPD': 'count'}).reset_index()
    state_summary.columns = ['Cust State', 'Total DPD', 'Entries Count']
    return summary, state_summary


def upload(request):
    if request.method == 'POST':
        form = uploadfileform(request.POST, request.FILES)
        if form.is_valid():
            if 'file' in request.FILES:
                summary, state_summary = sumry(request.FILES['file'])
                email_body =state_summary.to_string(index=False)
                send_mail(
                    'Python Assignment - Sparsh Manni',
                    email_body,
                    'smartaskk101@gmail.com',
                    ['sparsh1003@gmail.com', 'sprshmanni@gmail.com'],
                    fail_silently=False,
                )
                return render(request, 'success.html', {'summary': state_summary.to_html(index=False)})
            else:
                return HttpResponseBadRequest("File not uploaded.")
        else:
            return HttpResponseBadRequest("Invalid form submission.")
    else:
        form = uploadfileform()
    return render(request, 'upload.html', {'form': form})
