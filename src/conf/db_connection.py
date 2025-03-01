from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine, AsyncSession

engine: AsyncEngine = create_async_engine('sqlite+aiosqlite:///mini_chat.db')
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)