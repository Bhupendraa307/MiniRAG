import re
from datetime import datetime, timezone

ALLOWED_EXTENSIONS = {'.txt', '.md', '.pdf', '.docx'}

def clean_for_log(text):
    if not text:
        return ""
    cleaned = re.sub(r'[\r\n\t]', ' ', str(text))
    return cleaned[:200] + "..." if len(cleaned) > 200 else cleaned

def is_valid_file(filename):
    if not filename or '.' not in filename:
        return False
    ext = '.' + filename.lower().split('.')[-1]
    return ext in ALLOWED_EXTENSIONS

def utc_now():
    return datetime.now(timezone.utc)