"""NoctraX Pipeline - cat file.txt | noctrax — auto detect email/phone/username"""
import re, sys
EMAIL_RE = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_RE = re.compile(r'\+?\d{10,15}')
USERNAME_RE = re.compile(r'^[a-zA-Z0-9._-]{3,30}$')

def extract_targets(text):
    """Extract emails, phones, usernames from mixed file content"""
    emails = set(EMAIL_RE.findall(text))
    # phones: find candidates, then filter
    phone_candidates = PHONE_RE.findall(text)
    phones = set()
    for p in phone_candidates:
        clean = re.sub(r"[^\d+]", "", p)
        # must be 10-15 digits, if starts with + then ok else 10 digits
        digits = re.sub(r"\D", "", clean)
        if 10 <= len(digits) <= 15:
            # avoid random numbers like 1234567890 that are not phone? keep all
            if clean.startswith("+"):
                phones.add(clean)
            elif len(digits) == 10:
                # Indian 10 digit -> add +91 prefix for consistency
                phones.add("+91" + digits if not clean.startswith("+") else clean)
            else:
                phones.add(clean)
    # usernames: split by lines/commas/spaces, remove already matched emails/phones
    tokens = re.split(r'[\s,;\n\r\t]+', text)
    usernames = set()
    for tok in tokens:
        t = tok.strip().strip(",;")
        if not t or len(t) < 3 or len(t) > 30:
            continue
        if t in emails or t in phones:
            continue
        # skip if contains @ or is phone-like
        if "@" in t or PHONE_RE.fullmatch(t):
            continue
        # skip pure numbers
        if t.isdigit():
            continue
        # skip emails already
        if EMAIL_RE.fullmatch(t):
            continue
        # username pattern
        if USERNAME_RE.fullmatch(t):
            # avoid common words that are not usernames? keep simple: if token was on its own line and not email/phone, treat as username
            # heuristic: usernames usually don't contain spaces, and file likely has one per line
            usernames.add(t)
        # also handle @username case
        if t.startswith("@") and USERNAME_RE.fullmatch(t[1:]):
            usernames.add(t[1:])
    # Remove overlap: if token is email local part, don't double count
    # dedup already
    return list(emails), list(phones), list(usernames)

def detect_stdin():
    """Check if stdin has piped data"""
    if not sys.stdin.isatty():
        try:
            data = sys.stdin.read()
            if data and data.strip():
                return data
        except:
            pass
    return None

def detect_file_arg(arg):
    """If arg is a file path that exists, read it"""
    import pathlib
    p = pathlib.Path(arg)
    if p.is_file():
        try:
            return p.read_text(encoding="utf-8", errors="ignore")
        except:
            pass
    return None
