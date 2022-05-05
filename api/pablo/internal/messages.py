from core.queues.model import MessageContent


class LoadIpfsMessageContent(MessageContent):
    _COMMAND = 'LOAD_IPFS'
    cid: str
