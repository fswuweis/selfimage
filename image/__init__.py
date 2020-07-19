from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot import permission as perm

from .data_source import get_image_data

from hoshino import Service, R, priv
from hoshino.typing import *
from hoshino.util import DailyNumberLimiter, pic2b64, concat_pic, silence
from hoshino import util
from hoshino.modules.priconne import chara

__plugin_name__ = '识图'
__plugin_usage__ = r"""
以图识图
搜图 [图片]
识图 [图片]
image [图片]
[NLP模块] XXX搜图XXX图片XXX
""".strip()
sv = Service('image', enable_on_default=True, bundle='通用', help_=__plugin_usage__)
SAUCENAO_KEY = '3aa67c1500157dbaaa04407ed990a9eb21d40c79'#https://saucenao.com/自行申请


#@on_command('image', aliases=('image', '搜图', '识图', '搜圖', '識圖'), permission=perm.GROUP_ADMIN, only_to_me=False)
@sv.on_prefix(('识图', 'image', '搜图'))
async def image(session: CommandSession):
    pritnt('1111')
    image_data = session.get('image', prompt='图呢？GKD')
    pritnt(image_data)
    image_data_report = await get_image_data(image_data, SAUCENAO_KEY)
    pritnt(image_data_report)
    
    if image_data_report:
        await session.send(image_data_report)
    else:
        sv.logger.warning("Not found imageInfo")
        await session.send("[ERROR]Not found imageInfo")


@image.args_parser
async def _(session: CommandSession):
    image_arg = session.current_arg_images

    if session.is_first_run:
        if image_arg:
            session.state['image'] = image_arg[0]
        return

    if not image_arg:
        session.pause('没图说个J*，GKD!')

    session.state[session.current_key] = image_arg


@on_natural_language(keywords={'image', '搜图', '识图', '搜圖', '識圖'}, permission=perm.GROUP_ADMIN)
async def _(session: NLPSession):
    msg = session.msg
    return IntentCommand(90.0, 'image', current_arg=msg or '')