from typing import Any

from django.core.mail import get_connection, EmailMessage, EmailMultiAlternatives

from api.models import MailProvider
from api.schema import NewMailMessageIn, NewBulkMailMessageIn


class MailProviderNotFound(Exception):
    pass

class EmailService:
    def _get_mail_provider(self, from_email: str) -> MailProvider:
        mail_provider = MailProvider.objects.filter(
            from_email=from_email,
        )

        if not mail_provider.exists():
            raise MailProviderNotFound()

        return mail_provider.first()

    def _get_connection(self, mail_provider: MailProvider):
        return get_connection(
            host=mail_provider.host,
            port=mail_provider.port,
            username=mail_provider.host_user,
            password=mail_provider.host_password,
            use_tls=mail_provider.use_tls,
        )

    def _build_email(self, dto: NewMailMessageIn, connection: Any) -> EmailMultiAlternatives:
        email = EmailMultiAlternatives(
            subject=dto.subject,
            body=dto.body,
            from_email=dto.from_email,
            to=[dto.to],
            cc=[dto.cc] if dto.cc else None,
            bcc=[dto.bcc] if dto.bcc else None,
            connection=connection,
        )

        if dto.html_body:
            email.attach_alternative(dto.html_body, "text/html")

        for attachment in dto.attachments:
            email.attach(*attachment)

        return email

    def send_email(self, dto: NewMailMessageIn):
        mail_provider = self._get_mail_provider(dto.from_email)
        connection = self._get_connection(mail_provider)
        email = self._build_email(dto, connection)
        email.send()


    def send_bulk_email(self, dto: NewBulkMailMessageIn):
        mail_provider = self._get_mail_provider(dto.from_email)
        connection = self._get_connection(mail_provider)
        messages = [self._build_email(dto, connection) for dto in dto.messages]
        connection.send_messages(messages)


