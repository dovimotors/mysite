from django import forms

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
    StartDate = forms.DateTimeField(label='Start Date')
    EndDate = forms.DateTimeField(label='End Date')
    PaymentType = forms.ChoiceField(choices=PAYMENT_TYPE_CHOICES)
    Smoothing = forms.IntegerField(max_value=20,min_value=1)

