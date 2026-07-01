# from typing import List
#
# from fastapi import APIRouter, Depends, HTTPException,status,Path,Query
# from fastapi.responses import JSONResponse
#
# from users.models import UserModel
#
# router = APIRouter(prefix="/users", tags=["users"])
#
# @router.get("/", response_model=List[UserModel])
# async def