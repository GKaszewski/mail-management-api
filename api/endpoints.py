from typing import Optional, List

from ninja import Router, Form, UploadedFile, File
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from api.schema import NewMailMessageIn, NewBulkMailMessageIn
from api.services import EmailService, MailProviderNotFound

router = Router()
email_service = EmailService()


@router.post("/send-email", auth=JWTAuth())
def send_email(request, data: NewMailMessageIn):
    try:
        email_service.send_email(data)
        return {"status": "Email sent successfully"}
    except MailProviderNotFound:
        raise HttpError(404, "Mail provider not found")


@router.post("/send-email-form", auth=JWTAuth())
def send_email_form(request,
                    from_email: str = Form(...),
                    to: str = Form(...),
                    subject: str = Form(...),
                    body: str = Form(...),
                    html_body: Optional[str] = Form(None),
                    cc: Optional[str] = Form(None),
                    bcc: Optional[str] = Form(None),
                    attachments: List[UploadedFile] = File(default=[]),
                    ):
    try:
        _attachments = []
        for uploaded_file in attachments:
            content = uploaded_file.read()
            _attachments.append((uploaded_file.name, content, uploaded_file.content_type))

        dto = NewMailMessageIn(
            from_email=from_email,
            to=to,
            subject=subject,
            body=body,
            html_body=html_body,
            cc=cc,
            bcc=bcc,
            attachments=_attachments
        )

        email_service.send_email(dto)
        return {"status": "Email sent successfully"}
    except MailProviderNotFound:
        raise HttpError(404, "Mail provider not found")


@router.post("/send-bulk-email", auth=JWTAuth())
def send_bulk_email(request, data: NewBulkMailMessageIn):
    try:
        email_service.send_bulk_email(data)
        return {"status": "Bulk email sent successfully"}
    except MailProviderNotFound:
        raise HttpError(404, "Mail provider not found")