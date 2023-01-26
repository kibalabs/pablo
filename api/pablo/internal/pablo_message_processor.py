from core.exceptions import KibaException
from core.queues.message_queue_processor import MessageProcessor
from core.queues.model import Message

from pablo.internal.messages import ResizeImageMessageContent
from pablo.internal.pablo_manager import PabloManager


class PabloMessageProcessor(MessageProcessor):

    def __init__(self, pabloManager: PabloManager):
        self.pabloManager = pabloManager

    async def process_message(self, message: Message) -> None:
        if message.command == ResizeImageMessageContent.get_command():
            messageContent = ResizeImageMessageContent.parse_obj(message.content)
            await self.pabloManager.resize_image(imageId=messageContent.imageId)
            return
        raise KibaException(message='Message was unhandled')
