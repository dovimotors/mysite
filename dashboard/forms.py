from django import forms
import datetime

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

    todays_date = datetime.datetime.today()
    start_date = todays_date + datetime.timedelta(-10)
    todays_date = todays_date.strftime('%Y-%m-%d')
    start_date = start_date.strftime('%Y-%m-%d')


    Report = forms.ChoiceField(choices=REPORT_CHOICES)
    StartDate = forms.DateTimeField(label='Start Date',initial=start_date)
    EndDate = forms.DateTimeField(label='End Date',initial=todays_date)
    PaymentType = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES)
    Smoothing = forms.IntegerField(max_value=20,min_value=1,initial=20)
    BodyShop = forms.BooleanField(help_text='Check the box to show report using body shop data',initial=False,required=False)


