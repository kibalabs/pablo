import urllib.parse
from typing import Dict
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from core.requester import FileContent
from core.requester import HttpxFileTypes
from core.requester import KibaResponse
from core.requester import Requester
from core.util.typing_util import JSON


class IpfsRequester(Requester):

    def __init__(self, ipfsPrefix: str, headers: Optional[Dict[str, str]] = None, shouldFollowRedirects: bool = True):
        super().__init__(headers=headers, shouldFollowRedirects=shouldFollowRedirects)
        self.ipfsPrefix = ipfsPrefix
        self.ipfsHost = urllib.parse.urlparse(ipfsPrefix).netloc

    async def make_request(self, method: str, url: str, dataDict: Optional[JSON] = None, data: Optional[bytes] = None, formDataDict: Optional[Mapping[str, Union[str, FileContent]]] = None, formFiles: Optional[Sequence[Tuple[str, HttpxFileTypes]]] = None, timeout: Optional[int] = 10, headers: Optional[MutableMapping[str, str]] = None, outputFilePath: Optional[str] = None) -> KibaResponse:
        if url.startswith('ipfs://'):
            url = url.replace('ipfs://', self.ipfsPrefix, 1)
        return await super().make_request(method=method, url=url, dataDict=dataDict, data=data, formDataDict=formDataDict, formFiles=formFiles, timeout=timeout, headers=headers, outputFilePath=outputFilePath)
