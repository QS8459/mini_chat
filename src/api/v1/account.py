from src.conf.loging import log
from fastapi import Depends, APIRouter, status
from src.core.schema.account import AccountCreateSchema, AccountResponseSchema
from src.core.service.account.account import get_account_service, AccountService
from src.core.schema.responses import GlobalResponseSchema, serialize_orm
account_api: APIRouter = APIRouter(prefix='/account', tags=['account'])


@account_api.post('/', status_code=status.HTTP_201_CREATED, response_model= AccountResponseSchema)
async def add_account(
        data: AccountCreateSchema,
        service:AccountService = Depends(get_account_service)
):
    return await service.add(**data.dict())


@account_api.get('/', status_code=status.HTTP_200_OK, response_model=GlobalResponseSchema)
async def get_account_list(
        offset: int = 0,
        limit: int = 10,
        service: AccountService = Depends(get_account_service)
):
    count = await service.get_count()
    result = await service.get_all()
    serialized = serialize_orm(result, AccountResponseSchema)
    return {
        'count': count[0],
        'result': serialized
    }

@account_api.post('/login/')
async def login(
        email: str,
        password: str,
        service:AccountService=Depends(get_account_service)
):
    return await service.authenticate(email, password)