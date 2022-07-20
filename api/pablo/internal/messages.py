from core.queues.model import MessageContent


class ResizeImageMessageContent(MessageContent):
    _COMMAND = 'RESIZE_IMAGE'
    imageId: str
