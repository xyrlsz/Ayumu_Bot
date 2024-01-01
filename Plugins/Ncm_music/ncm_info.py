from Plugins.Ncm_music.post_request import post_request

# api_url = get_config("config.yaml")["api_url"]
api_url = "https://ncmapi.xyr.icu/"


def search_music_result(name: str) -> dict:
    url = api_url + "search?keywords=" + name
    result = post_request(url)
    return result["result"]["songs"]


# print(search_music_result("鸡你太美"))


def get_song_info(song_id: int) -> dict:
    url = api_url + "song/detail?ids=" + str(song_id)
    return post_request(url)["songs"][0]


# print(get_song_info(347230))
