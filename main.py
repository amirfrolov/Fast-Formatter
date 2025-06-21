from FastFormatter import FastFormatter
TITLE = "Fast Formatter"

COMPANY_MAIL = "@company.com"

def filter_user(val):
    return val.endswith(COMPANY_MAIL)

def filter_hash256(val):
    return len(val) == 64

def filter_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

def any_in(val, splitters):
    return any([i in splitters for i in val])

def filter_url(val : str):
    result = str()
    val = val.replace('[.]', '.').lower()
    if '.' in val and not any_in(val, '@ ') and not filter_ip(val):
        result = val    
    return result

def filter_email(val : str):
    return '@' in val and not any_in(val, ' []|*^"\'')


if __name__ == "__main__":
    # a = str()
    # a.startswith
    func_dict = {
        "user" : filter_user,
        "hash" : filter_hash256,
        "ip" : filter_ip,
        "url" : filter_url,
        "email": filter_email,
        "phone num" : lambda val : val.startswith("+972") or (len(val) == 10 and val.startswith("05")),
        "strip": lambda val : val.strip()
    }
    FastFormatter(func_dict, TITLE)
