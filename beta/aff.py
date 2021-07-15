from .. import chat_id, jdbot, _JdbotDir, logger
from telethon import events
import asyncio


@jdbot.on(events.NewMessage(from_users=chat_id, pattern=r'^/aff$'))
async def myaff(event):
    try:
        img_file = f"{_JdbotDir}/diy/aff.jpg"
        msg = await jdbot.send_message(chat_id, '感谢您的赞助', file=img_file)
        await asyncio.sleep(60)
        await jdbot.delete_messages(chat_id, msg)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))