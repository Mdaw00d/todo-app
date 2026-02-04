# Database package init file
from .session import get_db_session, get_async_session, engine
from .init import create_tables

# For backward compatibility, alias get_db_session as get_session
get_session = get_db_session

# For backward compatibility, alias create_tables as init_db
async def init_db():
    await create_tables()