from django import forms
# get the UniVerse imports
import os
os.chdir("C:\\U2\\XDEMO\\pythonbetarocket")
import u2py


def validateid(check_id):
    sub = u2py.Subroutine('VALIDATE_MEMBERS_ID', 4)
    sub.args[0] = check_id
    sub.call()
    if str(sub.args[2]) != '0':
        raise forms.ValidationError('Error! ' + str(sub.args[3]))


class MembersSearchForm(forms.Form):
    # UniVerse dict names
    uvfields = {
        1: "ID",
        2: "FIRST_NAME",
        3: "LAST_NAME",
        4: "ADDRESS",
        5: "CITY",
        6: "STATE_CODE",
    }
    # form field names, matching the UniVerse dict names
    formfields = {
        1: "member_id",
        2: "member_first_name",
        3: "member_last_name",
        4: "member_address",
        5: "member_city",
        6: "member_state_code",
    }
    # setting up the form
    member_id = forms.CharField(label='ID', required=False)
    member_first_name = forms.CharField(label='Name', required=False)
    member_last_name = forms.CharField(label='Surname', required=False)
    member_address = forms.CharField(label='Address', required=False)
    member_city = forms.CharField(label='City', required=False)
    member_state_code = forms.CharField(label='State Code', required=False)


class MembersResultForm(forms.Form):
    member_results = forms.ChoiceField(label='Results')


class MembersAdminForm(forms.Form):
    # UniVerse dict names
    uvfields = {
        1: "FIRST_NAME",
        2: "LAST_NAME",
        3: "ADDRESS",
        4: "CITY",
        5: "STATE_CODE",
    }
    # form field names, matching the UniVerse dict names
    formfields = {
        1: "member_first_name",
        2: "member_last_name",
        3: "member_address",
        4: "member_city",
        5: "member_state_code",
    }
    # setting up the form
    member_id = forms.CharField(label='ID')
    member_first_name = forms.CharField(label='Name')
    member_last_name = forms.CharField(label='Surname')
    member_address = forms.CharField(label='Address')
    member_city = forms.CharField(label='City')
    member_state_code = forms.CharField(label='State Code')

    def clean(self):
        cleaned_data = super(MembersAdminForm, self).clean()
        member_id = cleaned_data.get('member_id')
        # anything else than NEW must already exist
        if member_id != 'NEW':
            validateid(member_id)

        return self.cleaned_data


class MembersBankDetailForm(forms.Form):
    card_choices = (
        ('AMEX', 'American Express'),
        ('V', 'Visa'),
        ('MC', 'Mastercard'),
    )
    uvfields = {
        1: "CARDNUM",
        2: "CARDTYPE",
        3: "CARDEXP",
        4: "CARDSEC",
    }
    formfields = {
        1: "member_card_number",
        2: "member_card_type",
        3: "member_card_expiry",
        4: "member_card_cvv",
    }
    #
    member_id = forms.CharField(label='ID', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    member_card_number = forms.CharField(label='Card Number', max_length=16)
    member_card_type = forms.ChoiceField(label='Card Type', choices=card_choices)
    member_card_expiry = forms.CharField(label='Expiry Date')
    member_card_cvv = forms.CharField(label='CVV')
