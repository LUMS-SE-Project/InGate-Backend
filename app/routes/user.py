from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def path1():
    return {"message": "User Endpoint"}


@router.get('/{location}/items')
async def path2(location):
    return {"message": f"{location} Endpoint"}