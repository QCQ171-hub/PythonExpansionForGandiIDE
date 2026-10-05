# @block.name: BA视频解析器
import json


def get_video_info(json_str: str = "[]", index: int = 1) -> str:
    """
    【返回值】根据位置获取视频中所有信息，以JSON数组字符串形式返回。
    数组顺序固定为：[bvid, aid, title, author, play, danmaku, length, pic, desc]

    :param json_str: Bilibili 视频列表的原始 JSON 字符串
    :type json_str: str
    :param index: 视频在列表中的位置，从1开始计数
    :type index: int
    :return: 包含该视频所有字段值的JSON数组字符串，出错时返回空数组 "[]"
    :rtype: str
    """
    try:
        video_list = json.loads(json_str)
        if not isinstance(video_list, list):
            return "[]"
    except Exception:
        return "[]"

    # 转换为0基索引，并校验范围
    idx = int(index) - 1
    if idx < 0 or idx >= len(video_list):
        return "[]"

    item = video_list[idx]

    # 按固定顺序提取所有字段，None统一转为空字符串
    keys = ["bvid", "aid", "title", "author", "play", "danmaku", "length", "pic", "desc"]
    values = []
    for k in keys:
        val = item.get(k)
        if val is None:
            values.append("")
        else:
            # 清理标题中可能存在的HTML高亮标签
            s = str(val)
            s = s.replace('<em class="keyword">', '').replace('</em>', '')
            values.append(s)

    return json.dumps(values, ensure_ascii=False)


def get_group_info(json_str: str = "[]", index: int = 1) -> str:
    """
    【返回值】根据位置获取群聊中所有关键信息，以JSON数组字符串形式返回。
    数组顺序固定为：[id, title, member_count, unread_count, my_role, 
                     last_msg_content, last_msg_sender, last_msg_time, description]

    :param json_str: KukeChat 群聊列表的原始 JSON 字符串
    :type json_str: str
    :param index: 群在列表中的位置，从1开始计数
    :type index: int
    :return: 包含该群所有字段值的JSON数组字符串，出错时返回空数组 "[]"
    :rtype: str
    """
    try:
        group_list = json.loads(json_str)
        if not isinstance(group_list, list):
            return "[]"
    except Exception:
        return "[]"

    # 转换为0基索引，并校验范围
    idx = int(index) - 1
    if idx < 0 or idx >= len(group_list):
        return "[]"

    item = group_list[idx]

    # 按固定顺序提取字段，支持嵌套取值
    # 格式: (键名, 是否嵌套在last_message中)
    fields = [
        ("id", False),
        ("title", False),
        ("member_count", False),
        ("unread_count", False),
        ("my_role", False),
        ("content", True),       # last_message.content
        ("sender_display_name", True),  # last_message.sender_display_name
        ("created_at", True),    # last_message.created_at
        ("description", False)
    ]

    values = []
    for key, is_nested in fields:
        val = None
        if is_nested:
            last_msg = item.get("last_message")
            if isinstance(last_msg, dict):
                val = last_msg.get(key)
        else:
            val = item.get(key)

        # None 统一转为空字符串
        if val is None:
            values.append("")
        else:
            s = str(val)
            # 清理可能存在的HTML标签
            s = s.replace('<em class="keyword">', '').replace('</em>', '')
            values.append(s)

    return json.dumps(values, ensure_ascii=False)


# 显式地指定要暴露给 Scratch 的方法
__all__ = [
    'get_video_info',
    'get_group_info'
]