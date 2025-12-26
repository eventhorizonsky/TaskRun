from fastapi import APIRouter, Depends
from funboost.faas import fastapi_router as fb_router
from app.dependencies.auth import verify_token

router = APIRouter()
"""
Funboost Faas 相关接口路由
"""
router.include_router(fb_router, dependencies=[Depends(verify_token)])