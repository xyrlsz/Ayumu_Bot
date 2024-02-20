import re

# 给定的字符串
url_string = "https:\\/\\/www.bilibili.com\\/video\\/BV19G411S7mc?buvid=XYB620DBA99E4CB2962244FEDF927D28E11F4&from_spmid=tm.recommend.0.0&is_story_h5=false&mid=4QTxoVFNjoImg4zapQKXCw%3D%3D&p=1&plat_id=116&share_from=ugc&share_medium=android&share_plat=android&share_session_id=5c6999bf-80b4-4b98-bcce-a0f8d5ae85f2&share_source=QQ&share_tag=s_i&spmid=united.player-video-detail.0.0&timestamp=1700041116&unique_k=mFFCV0G&up_id=25406367&bbid=XYB620DBA99E4CB2962244FEDF927D28E11F4&ts=1700041117702"

# 使用正则表达式提取URL
pattern = re.compile(r'https://www\.bilibili\.com/video/[A-Za-z0-9]+')
match = pattern.search(url_string)

if match:
    extracted_url = match.group()
    print(extracted_url)
else:
    print("未找到匹配的URL")
