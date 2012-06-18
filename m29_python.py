import base64, string, random, json, httplib
import Crypto.Cipher.AES

def base64_encode_url(url):
    out = base64.b64encode(url)
    out = string.replace(out, '+', '-')
    out = string.replace(out, '/', '_')
    out = string.replace(out, '=', '')
    return out

def random_bytes(size):
    return "".join(chr(random.randrange(0, 256)) for i in range(size))

def get_m29_url(url):
    key1 = random_bytes(8)
    key2 = random_bytes(8)
    key = key1 + key2
    mode = Crypto.Cipher.AES.MODE_ECB
    aes  = Crypto.Cipher.AES.new( key, mode )
    block_size=16
    padding = '\0'
    pad = lambda s: s + (block_size - len(s) % block_size) * padding
    encrypted = aes.encrypt(pad(url))

    command = {'longUrlEncrypted': base64_encode_url(encrypted), 'firstKey': base64_encode_url(key1)}
    payload = json.dumps(command, ensure_ascii=False)
    headers = {'Content-Type': 'application/json'}
    conn = httplib.HTTPConnection('api.m29.us', 80)
    conn.request('POST', '/urlshortener/v1/url', payload, headers)
    response = conn.getresponse()
    data = None
    if response.status == 200:
        data = response.read()
    conn.close()

    if data is not None:
        decoded = json.loads(data)
        return decoded[u'id']+"/"+base64_encode_url(key2)
    else:
        return None

print get_m29_url("http://www.google.com")
