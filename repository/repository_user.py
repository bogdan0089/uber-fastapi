from sqlalchemy.ext.asyncio import AsyncSession
from schemas.schemas_user import RegisterUser, UserUpdate
from models.models import User
from sqlalchemy import select
from schemas.schemas_payment import PaymentMethod


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
    
    async def update_user(self, user: User, data: UserUpdate) -> User:
        for field, value in data.model_dump().items():
            setattr(user, field, value)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)

    async def deactive_user(self, user: User) -> bool:
        user.is_active = False
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def activated_user(self, user: User) -> bool:
        user.is_active = True
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update_avg_rating(self, user: User, avg: float) -> User:
        user.avg_rating = avg
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
    
    async def verify_email(self, user: User) -> bool:
        user.is_verified = True
        await self.session.flush()
        await self.session.refresh(user)

    async def get_users_for_admin(self, limit: int, offset: int) -> list[User]:
        users = await self.session.execute(
            select(User)
            .where(User.is_verified == True)
            .where(User.is_active == True)
            .limit(limit).offset(offset)
        )
        return users.scalars().all()
    
    async def payment_method(self, user: User, data: PaymentMethod):
        user.payment_id = data.payment_id
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        

    