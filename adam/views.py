from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from dbftopandas import AdamImport
from .models import ADAMFiles
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as lgout


def index(request):

    context = {}
    return render(request, 'mysite/index.html', context)

@login_required
def list(request):
    # main view for /adam/ app.  returns all paths in the database with links
    path_list = ADAMFiles.objects.all()
    context = {'path_list': path_list}
    return render(request, 'adam/index.html', context)


@login_required
def detail(request, path_id):
    # view for the adam/<id> page returns an html rendered dataframe
    # create the object to convert DBF to pandas
    # this view is mainly for previewing data
    ai = AdamImport()
    # get the id from the path and pull the correspoding DBF
    p = ADAMFiles.objects.get(id=path_id)
    p = str(p)
    # conver the DBF to a dataframe
    datafr = ai.DBFConverter(p,'output.csv','pandas')

    # *******************
    # modify the dataframe here before converting to HTML
    # be careful not to return too many rows or the http req will time out
    # *******************

    s = datafr.head()

    # *******************
    # *******************
    s_trunk = s.to_html()
    return HttpResponse(s_trunk)

@login_required
def export(request, path_id):
    # view to convert a DBF file on the fly and export it to a CSV
    ai = AdamImport()
    # get the id from the path and pull the correspoding DBF
    p = ADAMFiles.objects.get(id=path_id)
    p = str(p)
    ai.DBFConverter(p,'output.csv','csv')
    f = open('output.csv')
    ofile = os.path.basename(p)
    ofile = ofile.replace('.dbf','')
    ofile = ofile.replace('.DBF','')
    response = HttpResponse(f, content_type="text/csv")
    params = 'attachment; filename=%s.csv' % ofile
    response['Content-Disposition'] = params
    f.close()
    return response

@login_required
def test(request, path_id):
    p = ADAMFiles.objects.get(id=path_id)
    p = str(p)
    fp = os.path.basename(p)
    fp = fp.replace('.dbf','')
    return HttpResponse(fp)

def logout(request):
    lgout(request)
    return render(request,'registration/logout.html')