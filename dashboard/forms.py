from django import forms
import datetime

def get_todays_date():
    todays_date = datetime.datetime.today()
    todays_date = todays_date.strftime('%Y-%m-%d')
    return todays_date

def get_start_date(days_ago):
    start_date = datetime.datetime.today() + datetime.timedelta(days_ago)
    start_date = start_date.strftime('%Y-%m-%d')
    return start_date

class ServiceReports(forms.Form):
    C = 'C'
    I = 'I'
    W = 'W'
    E = 'E'
    all = 'all'
    PAYMENT_TYPE_CHOICES = (
        (C, 'Customer Pay'),
        (I, 'Internal'),
        (W, 'Warranty Pay'),
        (E, 'ESP Pay'),
        (all, 'All Payments')
    )
    ARO = 'ARO'
    Traffic = 'Traffic'
    Gross = 'Gross'
    REPORT_CHOICES = (
        (ARO, 'Averge Repair Order (Gross Sales)'),
        (Traffic, 'Count of ROs by day'),
        (Gross, 'Average gross profit by day'),
    )

    Report = forms.ChoiceField(choices=REPORT_CHOICES)
    StartDate = forms.DateTimeField(label='Start Date',initial=get_start_date(-10))
    EndDate = forms.DateTimeField(label='End Date',initial=get_todays_date())
    PaymentType = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES)
    Smoothing = forms.IntegerField(max_value=20,min_value=1,initial=20)
    BodyShop = forms.BooleanField(help_text='Check to show report using body shop data',initial=False,required=False)
    Export = forms.BooleanField(help_text='Check to output to csv rather than on screen',initial=False,required=False)

class PartsCoreReport(forms.Form):
    StartDate = forms.DateTimeField(label='Start Date',initial=get_start_date(-10))
    EndDate = forms.DateTimeField(label='End Date',initial=get_todays_date())

