import os
from fastapi import APIRouter
from fastapi import Depends
from pathlib import Path

from model.injector import get_auth_service, get_img_service
from model.models import AuthUser, SignUpUser
from model.verify_token import VerifyToken
from service.auth_service import AuthService
from service.img_service import ImageService

router = APIRouter()


@router.post('/login/')
async def login(form_data: AuthUser, auth_service: AuthService = Depends(get_auth_service)):
    tokens = await auth_service.authenticate_user(form_data)
    return tokens


@router.post('/signup/')
async def signup(form_data: SignUpUser, auth_service: AuthService = Depends(get_auth_service)):
    user = await auth_service.signup_user(form_data)
    return user


@router.post('/update/token')
async def update_token(username: str = Depends(VerifyToken(is_refresh=True)),
                       auth_service: AuthService = Depends(get_auth_service)):
    tokens = await auth_service.update_tokens(username)
    return tokens


@router.post('/logout')
async def logout(username: str = Depends(VerifyToken(is_refresh=False)),
                 auth_service: AuthService = Depends(get_auth_service)):
    await auth_service.delete_tokens(username)
    return {'msg': 'Logged out'}


@router.post('/generate_image')
async def get_posts(prompt: str,
                    username: str = Depends(VerifyToken(is_refresh=False)),
                    auth_service: ImageService = Depends(get_img_service)):
    parent = Path(__file__).parents[3]
    gen_files_dir = os.path.join(parent, 'generated')
    img_id = await auth_service.get_image_by_prompt(username, gen_files_dir, prompt)
    return {'prompt': prompt, 'imgs': [img_id]}
