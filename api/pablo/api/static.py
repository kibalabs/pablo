from core.exceptions import FoundRedirectException
from fastapi import APIRouter
from pablo.internal.model import CLOUDFRONT_URL

from pablo.internal.pablo_manager import PabloManager

# NOTE(krishan711): on cloudfront these would redirect automatically
def create_api(manager: PabloManager) -> APIRouter():  # pylint: disable=unused-argument
    router = APIRouter()

    @router.get('/images/{imagePath:path}')
    async def go_to_image(imagePath: str):
        raise FoundRedirectException(location=f'{CLOUDFRONT_URL}/static/images/{imagePath}')

    @router.get('/ipfs/{cid:path}')
    async def go_to_ipfs(cid: str):
        raise FoundRedirectException(location=f'{CLOUDFRONT_URL}/static/ipfs/{cid}')

    return router
