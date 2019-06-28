from urllib import request

# todo: do the retrieve bit after finishing the node.js restify bit

def get_street_view(query="tokyo"):
    r = request.urlretrieve("http://localhost:9966/", filename="temp")
    print(r)


if __name__ == "__main__":
    get_street_view()