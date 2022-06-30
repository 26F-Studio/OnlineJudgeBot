from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    support_platforms: dict = {
        "luogu": {"lg", "洛谷"},
    }
    luogu_question_types: dict = {
        "P": {"P", "主题库"},
        "B": {"B", "入门与面试"},
        "SP": {"SP", "S", "SPOJ"},
        "AT": {"AT", "A", "ATCODER"},
        "UVA": {"UVA", "UV", "U"},
    }
    luogu_question_ranges: dict = {
        "P": (1000, 8422),
        "B": (2001, 3641),
        "SP": (1, 34127),
        "AT": (26, 5809),
        "UVA": (100, 13292),
    }
