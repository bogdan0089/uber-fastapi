from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas_user import RegisterUser
from models.models import User
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class RepositoryUser:
    def __init__(self, session: AsyncSession):
        self.session = session



    async def register_user(self, data: RegisterUser, hashed: str) -> User:
        user = User(
            **data.model_dump(exclude={"password"}),
            hashed_password=hashed
        )
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user


    async def get_user_email(self, email: str) -> User:
        result = await self.session.execute(
            select(User)
            .where(User.email == email)
        )
        return result.scalars().first()
    

    async def get_user(self, user_id: int) -> User:
        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
            .where(User.is_active == True)
        )
        return result.scalars().first()
    

    async def get_users(self, limit, offset) -> list[User]:
        result = await self.session.execute(
            select(User)
            .limit(limit).offset(offset)
        )
        return result.scalars().all()
    

        