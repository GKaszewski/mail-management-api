# 📬 Mail Management API

This project provides an authenticated API for sending single and bulk emails using custom SMTP providers. Built with Django, Django Ninja, and JWT authentication.

---

## 🚀 Features

- ✅ Send single emails (plain text and HTML)
- ✅ Attach files via multipart/form
- ✅ Send bulk emails with multiple messages
- ✅ Auth-protected via JWT (`django-ninja-jwt`)
- ✅ Mail providers stored and managed via Django Admin

---


## 🔐 Authentication

1. **Login to get token:**

```http
POST /api/token/pair
Content-Type: application/json

{
  "username": "youruser",
  "password": "yourpass"
}
```

2. **Use the token to access protected endpoints:**

```http
Authorization: Bearer <access_token>
```

---

## ✉️ Sending Emails

### 🔹 Single Email (JSON)

```http
POST /api/send-email
Authorization: Bearer <token>
Content-Type: application/json

{
  "from_email": "sender@example.com",
  "to": "recipient@example.com",
  "subject": "Hello",
  "body": "This is a plain text fallback",
  "html_body": "<p>This is <strong>HTML</strong></p>",
  "cc": null,
  "bcc": null,
  "attachments": []
}
```

---

### 🔹 Single Email (multipart/form)

```bash
curl -X POST http://localhost:8000/api/send-email-form \
  -H "Authorization: Bearer <token>" \
  -F "from_email=sender@example.com" \
  -F "to=recipient@example.com" \
  -F "subject=Hello" \
  -F "body=Hello plain" \
  -F "html_body=<h1>HTML</h1>" \
  -F "attachments=@file.pdf"
```

---

### 🔹 Bulk Email (JSON)

```http
POST /api/send-bulk-email
Authorization: Bearer <token>
Content-Type: application/json

{
  "from_email": "sender@example.com",
  "messages": [
    {
      "from_email": "sender@example.com",
      "to": "a@example.com",
      "subject": "Hi A",
      "body": "Hello A!",
      "attachments": []
    },
    {
      "from_email": "sender@example.com",
      "to": "b@example.com",
      "subject": "Hi B",
      "body": "Hello B!",
      "attachments": []
    }
  ]
}
```

## 🛠 Mail Provider Setup

Add mail provider entries via Django Admin:

| Field           | Example             |
| --------------- | ------------------- |
| `host`          | `smtp.gmail.com`    |
| `port`          | `587`               |
| `use_tls`       | ✅ (True)            |
| `host_user`     | `user@gmail.com`    |
| `host_password` | `your_app_password` |
| `from_email`    | `user@gmail.com`    |
