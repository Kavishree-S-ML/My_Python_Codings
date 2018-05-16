import urllib

# url = "https://images.pexels.com/photos/67636/rose-blue-flower-rose-blooms-67636.jpeg"
url = "https://images.pexels.com/photos/67636/rose-blue-flower-rose-blooms-67636.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940"
filename = "image.jpeg"
urllib.urlretrieve(url, filename)

