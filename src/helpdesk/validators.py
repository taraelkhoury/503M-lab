# validators.py
#
# Validators for file uploads.

from pathlib import Path

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from helpdesk import settings as helpdesk_settings


def validate_file_extension(value):
    if not helpdesk_settings.HELPDESK_VALIDATE_ATTACHMENT_TYPES:
        return

    filename = value.name

    # Reject filenames containing directory separators.
    if "/" in filename or "\\" in filename:
        raise ValidationError(_("Invalid filename."))

    # Reject filenames with multiple extensions or no extension.
    if filename.count(".") != 1 or filename.startswith("."):
        raise ValidationError(_("Invalid filename or multiple extensions."))

    # Check the final extension against the allowlist.
    ext = Path(filename).suffix.lower()

    if ext not in helpdesk_settings.HELPDESK_VALID_EXTENSIONS:
        raise ValidationError(_("Unsupported file extension: ") + ext)

def validate_file_content(value):
    from django.core.exceptions import ValidationError
    from django.utils.translation import gettext as _

    filename = value.name.lower()

    if filename.endswith(".png"):
        position = value.tell()
        try:
            value.seek(0)
            signature = value.read(8)
        finally:
            value.seek(position)

        if signature != b"\x89PNG\r\n\x1a\n":
            raise ValidationError(_("Invalid PNG file content."))