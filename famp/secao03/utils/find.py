from re import X


def find(arr: list, id):
    for item in arr:
        if item.id == id:
            return item

def findID(arr: list, id):
    for item in arr:
        if item.id == id:
            return item.id