import hashlib

caracteres = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
url = "https://forms.layers.education/_descobrir1_L9tB4sE0RzVp7KfG_descobrir2_QhU?answ=8d1ac76"

true_hash = "dbb47698e913d9d55b3ade4b31b187a4" 

tries = 0
find_url = ""
for x in caracteres:
    for y in caracteres:
        tries += 1
        url_test = url.replace('_descobrir1_', x).replace('_descobrir2_', y)
        url_hash = hashlib.md5(url_test.encode()).hexdigest()
        
        if (true_hash == url_hash):
            print("Url encontrada! Tentativas:", tries, "URL:", url_test)
            find_url = url_test
            break

print("Url encontrada:", find_url)