from mitmproxy import http


def request(flow):
    if "f1ag" in flow.request.url:
        flow.response = http.HTTPResponse.make(403, b"Nice try :),but plz dont try again.\n")
