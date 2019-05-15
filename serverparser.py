from difflib import SequenceMatcher


def get_matched_key(phrase, dictionary):
    phrase = phrase.lower()

    best_key = None
    best_ratio = 0
    for key in dictionary:
        ratio = SequenceMatcher(None, phrase, dictionary[key].lower()).ratio()
        if ratio > best_ratio:
            best_key = key
            best_ratio = ratio
    return best_key, best_ratio


def extract_server(phrase):
    split = phrase.replace("colon", "port").replace(":", "port").split("port")
    if not split:
        return None

    ip = split[0].lower().replace("dot", ".")
    while " " in ip:
        ip = ip.replace(" ", "")

    if len(split) > 1:
        port = split[1]
        while " " in port:
            port = port.replace(" ", "")

        try:
            int(port)
        except ValueError:
            return ip
        return ip + ":" + port
    return ip


def ip_to_spoken(ip):
    return ip.replace(".", " dot ")
