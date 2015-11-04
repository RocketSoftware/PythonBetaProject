from django.shortcuts import render
from .forms import MembersSearchForm, MembersBankDetailForm, MembersAdminForm, MembersResultForm
from .models import readmember, writemember, searchmember
# get the UniVerse imports
import os
os.chdir("C:\\U2\\XDEMO\\pythonbetarocket")
import u2py


# Create your views here.
def get_member(request):
    title = 'Members Search'
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if request.POST.get("search"):
            form = MembersSearchForm(request.POST)
            uvfields = MembersSearchForm.uvfields
            formfields = MembersSearchForm.formfields
            context = {
                'title': title,
                'form': form,
            }
            if form.is_valid():
                formdata = form.cleaned_data
                if formdata.get('member_id') == 'NEW':
                    form = MembersAdminForm(initial=None)
                else:
                    readmember(formdata, uvfields, formfields)
                    # set the form data and render again
                    form = MembersAdminForm(initial=formdata)
                context = {
                    'title': title,
                    'form': form,
                    'update': "update",
                    'bankenabled': "bankenabled"
                }
        elif request.POST.get("update"):
            form = MembersSearchForm(request.POST)
            uvfields = MembersSearchForm.uvfields
            formfields = MembersSearchForm.formfields
            context = {
                'title': title,
                'form': form,
            }
            if form.is_valid():
                formdata = form.cleaned_data
                writemember(formdata, uvfields, formfields)
                member_id = formdata.get('member_id')
                # reset the form to go back to search form
                form = MembersSearchForm()
                message = member_id + " Updated Successfully!"
                context = {
                    'title': title,
                    'form': form,
                    'message': message,
                    'update': "",
                    'bankenabled': "",
                }
        elif request.POST.get("bankdetail"):
            form = MembersBankDetailForm(request.POST)
            uvfields = MembersBankDetailForm.uvfields
            context = {
                'title': title,
                'form': form,
            }
            if form.is_valid():
                formdata = form.cleaned_data
                readmember(formdata, uvfields)
                # set the form data and render again
                form = MembersBankDetailForm(initial=formdata)
                context = {
                    'title': title,
                    'form': form,
                    'update': "update",
                    'bankenabled': "bankenabled"
                }
        else:
            form = MembersSearchForm()
            context = {
                "title": title,
                "form": form,
                'value': "Get Member",
                'update': "",
                'bankenabled': "",
            }
    else:
        form = MembersSearchForm()
        context = {
            "title": title,
            "form": form,
            'value': "Get Member",
            'update': "",
            'bankenabled': "",
        }

    return render(request, "members.html", context)
