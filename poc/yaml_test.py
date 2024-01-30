import yaml

data = {
    'hash' : "",
    'type': "content",
    'comment': "merged to top",
    'original': "asdfasfasdf\nasdfasfdasdf\n asdfasdfasdf",
    'kr': "가나다라마바(:asdf)\n가나다라\nㅁㄴㅇㄹㅁㄴㅇㄹ",
    'null' : None
}

yaml_data = yaml.dump(data, default_style='|',allow_unicode=True,sort_keys=False)

print(yaml_data)

loaded_data = yaml.load(yaml_data, Loader=yaml.SafeLoader)

print(loaded_data)