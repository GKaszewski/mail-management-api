import smtplib

from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from api.models import MailProvider

class MailProviderForm(forms.ModelForm):
    host_password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = MailProvider
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        host = cleaned_data.get("host")
        port = cleaned_data.get("port")
        user = cleaned_data.get("host_user")
        password = cleaned_data.get("host_password")
        use_tls = cleaned_data.get("use_tls")

        if host and port and user and password:
            try:
                connection = smtplib.SMTP(host, port, timeout=10)
                if use_tls:
                    connection.starttls()
                connection.login(user, password)
                connection.quit()
            except Exception as e:
                raise ValidationError(f'Could not connect to the mail server: {e}')
        return cleaned_data

@admin.register(MailProvider)
class MailProviderAdmin(admin.ModelAdmin):
    form = MailProviderForm
    list_display =  ("from_email", "host", "port", "use_tls")
    search_fields = ("from_email", "host_user", "host")
    list_filter = ("use_tls",)

    fieldsets = (
        (None, {
            "fields": ("from_email", "host", "port", "use_tls")
        }),
        ("Authentication", {
            "fields": ("host_user", "host_password")
        }),
    )