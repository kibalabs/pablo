from core.exceptions import FoundRedirectException
from fastapi import APIRouter

from pablo.internal.model import SERVING_URL
from pablo.internal.pablo_manager import PabloManager


# NOTE(krishan711): on cloudfront these would redirect automatically
def create_api(manager: PabloManager) -> APIRouter():  # pylint: disable=unused-argument
    router = APIRouter()

    # TODO(krishan711): these would be better using servingUrl instead of hard-coding

    @router.get('/images/{imagePath:path}')
    async def go_to_image(imagePath: str) -> None:
        raise FoundRedirectException(location=f'{SERVING_URL}/static/images/{imagePath}')

    @router.get('/ipfs/{cid:path}')
    async def go_to_ipfs(cid: str) -> None:
        raise FoundRedirectException(location=f'{SERVING_URL}/static/ipfs/{cid}')

    return router
