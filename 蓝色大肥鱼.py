import ast
import math
import re
from datetime import datetime

USER_PREFIX = "你："
AI_PREFIX = "ai："

TEXT = {
    "zh": {
        "welcome": "欢迎使用蓝色大肥鱼ai助手！",
        "empty": "请输入内容后再试。",
        "beyond": "啊哦，这个问题有点超纲了，请换个问题吧",
        "switch_english": "ok!",
        "switch_chinese": "好的！",
        "goodbye": "bye!",
        "zaijian": "再见啦！",
        "language_mode": "当前是中文模式。输入 Can you speak English? 可以切换到英文。",
        "datetime": "",
        "how_are_you": "我运行得很好，随时准备陪你聊天。你今天过得怎么样？",
        "identity": "我是蓝色大肥鱼 AI 助手，一个完全在本地运行的 Python 小助手。我能陪你聊天、回答简单问题，也能计算基础数学算式。",
        "capabilities": "我可以计算基础数学算式，支持加、减、乘、除和括号；也能进行简单的中英文聊天，还能告诉你本地时间和日期。",
        "greeting": "你好呀！我是蓝色大肥鱼 AI 助手。想聊点什么，或者算一道数学题？",
        "thanks": "不客气，能帮到你就好！",
        "apology": "没关系，别放在心上。",
        "praise": "谢谢夸奖，我会继续努力的！",
        "positive": "听到你心情不错，我也跟着开心起来了！",
        "negative": "听起来你现在不太好受。先做个深呼吸，别着急；如果愿意，可以慢慢和我说说。",
        "farewell": "拜拜！想退出时输入“再见”就好。"
    },
    "en": {
        "welcome": "Welcome to the Blue Big Fat Fish AI Assistant!",
        "empty": "Please enter something and try again.",
        "beyond": "Oops, this question is a bit beyond my current abilities. Please try another one.",
        "switch_english": "ok!",
        "switch_chinese": "好的！",
        "goodbye": "bye!",
        "zaijian": "再见啦！",
        "language_mode": "I'm currently in English mode. Type 你能说中文吗？ to switch to Chinese.",
        "datetime": "",
        "how_are_you": "I'm running well and ready to chat. How has your day been?",
        "identity": "I'm the Blue Big Fat Fish AI Assistant, a small Python helper running entirely on your device. I can chat, answer simple questions, and solve basic math.",
        "capabilities": "I can solve basic math with addition, subtraction, multiplication, division, and parentheses. I can also have simple chats in Chinese or English and tell you the local time and date.",
        "greeting": "Hi there! I'm the Blue Big Fat Fish AI Assistant. Want to chat, or shall we solve a math problem?",
        "thanks": "You're welcome. Glad I could help!",
        "apology": "No worries at all.",
        "praise": "Thank you for the kind words. I'll keep doing my best!",
        "positive": "I'm glad to hear you're feeling good!",
        "negative": "I'm sorry you're feeling this way. Take a slow breath and don't rush yourself. If you'd like, you can tell me what's going on.",
        "farewell": "See you! Type Goodbye. whenever you want to exit."
    }
}

CHAT_KEYWORDS = {
    "zh": {
        "language_mode": ("语言模式", "什么语言", "当前语言", "说的语言", "说中文吗", "说英文吗", "说英语吗", "中文还是英文", "中文模式", "英文模式", "英语模式"),
        "datetime": ("现在几点", "几点", "现在时间", "当前时间", "时间是多少", "时间", "日期", "几号", "星期几", "周几", "今天几月", "今天星期", "什么时候"),
        "how_are_you": ("你好吗", "最近怎么样", "你怎么样", "过得怎么样", "你还好吗"),
        "identity": ("你是谁", "你叫什么", "你的名字", "介绍一下你", "介绍自己", "你是机器人吗", "你是什么"),
        "capabilities": ("你能做什么", "你会做什么", "你会什么", "能帮我什么", "功能", "帮助"),
        "greeting": ("你好", "您好", "哈喽", "嗨", "早上好", "上午好", "中午好", "下午好", "晚上好", "早安"),
        "thanks": ("谢谢", "多谢", "感谢", "辛苦了"),
        "apology": ("对不起", "抱歉", "不好意思"),
        "praise": ("你真棒", "你好厉害", "太厉害了", "真聪明", "喜欢你"),
        "positive": ("开心", "高兴", "快乐", "兴奋", "太好了", "哈哈"),
        "negative": ("难过", "伤心", "不开心", "郁闷", "焦虑", "压力", "累", "孤独", "害怕", "烦"),
        "farewell": ("拜拜", "晚安", "回头见", "下次见")
    },
    "en": {
        "language_mode": ("language mode", "what language", "which language", "current language", "speak chinese", "speak english", "english or chinese"),
        "datetime": ("what time", "current time", "local time", "time now", "time", "what date", "current date", "today's date", "date", "today", "what day is it", "what is the date", "what's the date"),
        "how_are_you": ("how are you", "how are you doing", "how's it going", "how is it going", "how do you feel"),
        "identity": ("who are you", "what are you", "your name", "introduce yourself", "tell me about yourself", "are you a robot"),
        "capabilities": ("what can you do", "what do you do", "capabilities", "your features", "help me", "help"),
        "greeting": ("hello", "hi", "hey", "good morning", "good afternoon", "good evening"),
        "thanks": ("thanks", "thank you", "thx", "appreciate it"),
        "apology": ("sorry", "my apologies", "apologize"),
        "praise": ("you're great", "you are great", "awesome", "amazing", "good job", "well done"),
        "positive": ("happy", "glad", "excited", "great news", "feeling good"),
        "negative": ("sad", "unhappy", "depressed", "anxious", "stressed", "tired", "lonely", "afraid", "upset", "feeling bad"),
        "farewell": ("bye", "see you", "good night", "talk later")
    }
}

CHAT_ORDER = (
    "language_mode",
    "datetime",
    "how_are_you",
    "identity",
    "capabilities",
    "greeting",
    "thanks",
    "apology",
    "praise",
    "positive",
    "negative",
    "farewell"
)


def get_text(language, key):
    return TEXT[language][key]


def canonical_command(user_input):
    normalized = user_input.strip().casefold()
    return normalized.rstrip(" .!?。！？\t\r\n")


def is_math_candidate(expression):
    stripped = expression.strip()
    if not stripped or len(stripped) > 120:
        return False
    if not any(character.isdigit() for character in stripped):
        return False
    allowed = set("0123456789.+-*/() \t")
    return all(character in allowed for character in stripped)


def evaluate_node(node):
    if isinstance(node, ast.Constant):
        if type(node.value) is int or type(node.value) is float:
            return node.value
        raise ValueError
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = evaluate_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return value
        return -value
    if isinstance(node, ast.BinOp):
        left = evaluate_node(node.left)
        right = evaluate_node(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        raise ValueError
    raise ValueError


def evaluate_math(expression):
    if not is_math_candidate(expression):
        return None
    try:
        tree = ast.parse(expression.strip(), mode="eval")
        value = evaluate_node(tree.body)
    except (SyntaxError, ValueError, TypeError, ZeroDivisionError, OverflowError, RecursionError, MemoryError):
        return None
    if type(value) is float and not math.isfinite(value):
        return None
    return value


def format_number(value):
    if type(value) is int:
        return str(value)
    if value == 0:
        return "0"
    rounded = round(value, 12)
    if rounded.is_integer():
        return str(int(rounded))
    return format(rounded, ".12g")


def contains_keyword(text, keyword, language):
    if language == "zh":
        return keyword in text
    pattern = r"(?<![a-z])" + re.escape(keyword) + r"(?![a-z])"
    return re.search(pattern, text) is not None


def matches_any(text, keywords, language):
    return any(contains_keyword(text, keyword, language) for keyword in keywords)


def local_datetime_reply(language):
    now = datetime.now()
    if language == "zh":
        weekdays = ("星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日")
        return "现在是 {0}年{1:02d}月{2:02d}日 {3} {4:02d}:{5:02d}:{6:02d}。".format(
            now.year, now.month, now.day, weekdays[now.weekday()], now.hour, now.minute, now.second
        )
    return "The local time is {0:04d}-{1:02d}-{2:02d} {3:02d}:{4:02d}:{5:02d} ({6}).".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second, now.strftime("%A")
    )


def chat_reply(user_input, language):
    lowered = user_input.casefold()
    other_language = "en" if language == "zh" else "zh"
    for category in CHAT_ORDER:
        current_match = matches_any(lowered, CHAT_KEYWORDS[language][category], language)
        other_match = matches_any(lowered, CHAT_KEYWORDS[other_language][category], other_language)
        if current_match or other_match:
            if category == "datetime":
                return local_datetime_reply(language)
            return get_text(language, category)
    return None


def main():
    language = "zh"
    print(get_text(language, "welcome"))
    while True:
        try:
            raw_input = input(USER_PREFIX)
        except (EOFError, KeyboardInterrupt):
            print()
            break
        user_input = raw_input.strip()
        command = canonical_command(user_input)
        if command == "goodbye":
            print(AI_PREFIX + get_text(language, "goodbye"))
            break
        if command == "再见":
            print(AI_PREFIX + get_text(language, "zaijian"))
            break
        if command == "can you speak english":
            language = "en"
            print(AI_PREFIX + get_text(language, "switch_english"))
            continue
        if command == "你能说中文吗":
            language = "zh"
            print(AI_PREFIX + get_text(language, "switch_chinese"))
            continue
        if not user_input:
            print(AI_PREFIX + get_text(language, "empty"))
            continue
        if is_math_candidate(user_input):
            result = evaluate_math(user_input)
            if result is not None:
                print("{0}{1} = {2}".format(AI_PREFIX, user_input, format_number(result)))
                continue
        reply = chat_reply(user_input, language)
        if reply is None:
            reply = get_text(language, "beyond")
        print(AI_PREFIX + reply)


if __name__ == "__main__":
    main()
