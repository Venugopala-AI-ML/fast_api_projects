import os
import re
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import Optional

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str, min_length: int = 8) -> None:
    """Validate password strength.

    Raises:
        ValueError: If the password does not meet strength requirements.
    """

    errors = []
    if len(password) < min_length:
        errors.append(f"at least {min_length} characters")
    if not re.search(r"[A-Za-z]", password):
        errors.append("at least one letter")
    if not re.search(r"\d", password):
        errors.append("at least one digit")
    # match any character that is not a letter/digit/underscore
    if not re.search(r"[^A-Za-z0-9]", password):
        errors.append("at least one special character")

    if errors:
        raise ValueError("Password must contain " + ", ".join(errors))


def send_otp_email(to_email: str, otp: str, subject: Optional[str] = None) -> None:
    """Send an OTP email to the specified address.

    This uses environment variables for SMTP configuration. If no SMTP
    settings are provided, the OTP is printed to stdout for local testing.
    """

    subject = subject or "Your password reset code"

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "0") or 0)
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_use_tls = os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")
    from_email = os.getenv("EMAIL_FROM", "noreply@example.com")

    body = f"Your verification code is: {otp}\n\nIf you did not request this, you can ignore this message."

    # If SMTP settings are not configured, fall back to printing.
    if not smtp_host or smtp_port == 0:
        print(f"[OTP] To: {to_email} | Subject: {subject} | Body: {body}")
        return

    message = EmailMessage()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
        if smtp_use_tls:
            server.starttls()
        if smtp_user and smtp_pass:
            server.login(smtp_user, smtp_pass)
        server.send_message(message)


def create_jwt_token(payload: dict):
    # Implementation for creating JWT token
    pass