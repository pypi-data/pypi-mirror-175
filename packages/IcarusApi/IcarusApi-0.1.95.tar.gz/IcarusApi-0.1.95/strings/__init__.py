def match(text: str, left: str, right: str) -> list:
    """
    匹配文本中满足条件的全部文本（正则实现）\n
    e.g.
    \t match("abc aqc","a", "c") \n
    \t result: ["b","q"] \n
    :param text: 需要匹配的文本
    :param left: 左侧文本
    :param right: 右侧文本
    :return: 返回包含结果的字符串列表
    """
    ...


def replace(text: str, old: str, new: str, num=-1) -> list:
    """
    字符串替换\n
    :param text: 文本
    :param old: 原始字符串
    :param new: 替换字符串
    :param num: 替换次数，可省略，默认-1为全部替换
    :return:
    """
    ...


def extend(text: str, recursion: bool, delims: tuple) -> list:
    """
    按格式扩展字符串\n
    eg. \n
    a[1-3]b 扩展得到 ["a1b","a2b","a3b"]\n
    :param text: 文本
    :param recursion: 是否递归，可省略，默认false，当文本有多个扩展标记时可以开启
    :param delims: 扩展标记，可省略，默认 ("[","-","]")
    :return:
    """
    ...


def format(format_str: str, *args) -> str:
    """
    格式化字符串\n
    :return:
    """


def format_split(text: str, format_str: str, lsep="{", rsep="}") -> str:
    """
    格式化切分字符串\n
    e.g. \n
    format_split("ABCDE","A{hello}C{world}E")\n
    [{\n
    "hello":"B",\n
    "world":"D\n
    }]\n
    :param text: 文本
    :param format_str: 格式字符串
    :param lsep: 左变量标记符,
    :param rsep: 右变量标记符
    :return:
    """
    ...
