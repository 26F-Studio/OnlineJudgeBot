import random

from nonebot import get_driver, on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Arg, ArgPlainText, ArgStr, CommandArg
from nonebot.rule import to_me

from .config import Config
from .luogu import get_question_info

global_config = get_driver().config
config = Config.parse_obj(global_config)

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

command_help = on_command("help", aliases={"?", "帮助"})
luogu = on_command("luogu", aliases=config.support_platforms["luogu"])


@command_help.handle()
async def _():
    msg = Message('''Command List: \n''')
    msg.append('''/<help|?|帮助>\n''')
    msg.append('''    # Show this message\n''')
    msg.append('''/<luogu|lg|洛谷> [question_type] [question_number]\n''')
    msg.append('''    # Display question info, randomized if not provided\n''')
    msg.append('''    question_type - Question type: <P|B|SP|AT|UVA>\n''')
    msg.append('''    question_number - Question number (int)\n''')
    await command_help.finish(msg)


@luogu.handle()
async def _(arg_message: Message = CommandArg()):
    args_plain = arg_message.extract_plain_text()
    args = args_plain.split(" ")

    question_type = random.choice(list(config.luogu_question_types.keys()))
    if len(args) > 0 and args[0]:
        found = False
        for temp_type, temp_aliases in config.luogu_question_types.items():
            if args[0].upper() in temp_aliases:
                question_type = temp_type
                found = True
                break
        if not found:
            await luogu.reject(f"题目类型 {args[0]} 非法")
            return

    question_id = random.randrange(*config.luogu_question_ranges[question_type])
    if len(args) > 1 and args[1]:
        if not args[1].isdigit():
            await luogu.reject(f"题目编号 {args[1]} 非法")
            return
        question_id = int(args[1])

    if question_id not in range(*config.luogu_question_ranges[question_type]):
        await luogu.reject(f"题目编号 {question_type}{question_id} 不在洛谷题库内")
    else:
        link, img = await get_question_info(f"{question_type}{question_id}")
        msg = Message(link)
        if img is not None:
            msg.append(MessageSegment.image(img))
        await luogu.finish(msg)
