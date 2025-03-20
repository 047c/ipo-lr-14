import json

def spSearch(filename="shop/files/dump.json", by_id=None):
    dump = "bad: not exist"
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            dump = json.load(file)
    except FileNotFoundError:
        return dump

    result = ""
    search_status = False

    if by_id is None:
        for item in dump:
            if item['model'] == 'data.specialty':
                result = f"{result}<h1>{item['fields']['title']}</h1><h2>Тип: {item['fields']['c_type']}</h2><h2>Код: {item['fields']['code']}</h2>"
                search_status = True
    else:
        for item in dump:
            if item["model"] == "data.specialty":
                if item["fields"]["code"] == by_id:
                    result = f"<h1>{item['fields']['title']}</h1><h2>Тип: {item['fields']['c_type']}</h2><h2>Код: {item['fields']['code']}</h2>"
                    search_status = True
    if (search_status == False):
        result = "<h1>Ошибка! Указанный id не существует</h1>"
    return result
