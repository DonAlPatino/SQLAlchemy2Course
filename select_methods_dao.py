from pydantic import EmailStr, create_model
from sqlalchemy.ext.asyncio import AsyncSession

from dao.dao import UserDAO
from asyncio import run
from dao.session_maker import connection
from models import User
from schemas import UserPydantic, UsernameIdPydantic


@connection
async def select_all_users(session):
    return await UserDAO.get_all_users(session)


# all_users = run(select_all_users())
# for i in all_users:
#     data = {'username': i.username, 'password': i.password, 'email': i.email}
#     print(data)

# for i in all_users:
#     print(i.to_dict())

# for i in all_users:
#     user_pydantic = UserPydantic.from_orm(i)
#     print(user_pydantic.dict())


@connection
async def select_username_id(session):
    return await UserDAO.get_username_id(session)


# rez = run(select_username_id())
# for i in rez:
#     data = {'user_id': i[0], 'username': i[1]}
#     print(data)

# rez = run(select_username_id())
# for i in rez:
#     rez = UsernameIdPydantic.from_orm(i)
#     print(rez.dict())

@connection(isolation_level="READ COMMITTED", commit=False)
async def select_full_user_info(session, user_id: int):
    # rez = await UserDAO.get_user_info(session=session, user_id=user_id)
    rez = await UserDAO.find_one_or_none_by_id(session=session, data_id=user_id)
    if rez:
        return UserPydantic.from_orm(rez).dict()
    return {'message': f'Пользователь с ID {user_id} не найден!'}


async def myrun():
    info = await select_full_user_info(user_id=1)
    print(info)
    # {'username': 'yakvenalex', 'email': 'example@example.com', 'profile': None}

    info = await select_full_user_info(user_id=4)
    print(info)
    # {'username': 'john_doe', 'email': 'john.doe@example.com', 'profile': {'first_name': 'John', 'last_name': 'Doe', 'age': 28, 'gender': 'мужчина', 'profession': 'инженер', 'interests': ['hiking', 'photography', 'coding'], 'contacts': {'phone': '+123456789', 'email': 'john.doe@example.com'}}}

    info = await select_full_user_info(user_id=1113)
    print(info)
    # {'message': 'Пользователь с ID 1113 не найден!'}

    return {'finished'}


# res = run(myrun())
# print(res)


@connection(commit=False)
async def select_full_user_info_email(session: AsyncSession, user_id: int, email: str):
    FilterModel = create_model(
        'FilterModel',
        id=(int, ...),
        email=(EmailStr, ...)
    )

    user = await UserDAO.find_one_or_none(session=session, filters=FilterModel(id=user_id, email=email))

    if user:
        # Преобразуем ORM-модель в Pydantic-модель и затем в словарь
        return UserPydantic.model_validate(user).model_dump()

    return {'message': f'Пользователь с ID {user_id} не найден!'}


# info = run(select_full_user_info_email(user_id=21, email='bob.smith@example.com'))
# print(info)

@connection()
async def select_all_users(session):
    result = await UserDAO.find_all(session=session, filters=None)
    if result:
        return result
    return {'message': f'Пользователь с ID не найден!'}


# rez = run(select_all_users())
# for i in rez:
#     rez = UsernameIdPydantic.from_orm(i)
#     print(rez.dict())


# @connection(commit=False)
# async def get_select(session: AsyncSession, user_id: int):
#     user = await session.get(User, user_id)
#     print(UserPydantic.model_validate(user).model_dump())
#
# # run(get_select(user_id=21))

@connection(commit=False)
async def get_select(session: AsyncSession, user_id: int):
    user = await UserDAO.find_one_or_none_by_id(session=session, data_id=user_id)
    print(UserPydantic.model_validate(user).model_dump())

run(get_select(user_id=21))