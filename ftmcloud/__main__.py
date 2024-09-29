import asyncio
import os

import uvicorn

from ftmcloud.cross_cutting.db.db import initiate_database

if __name__ == '__main__':
    asyncio.run(initiate_database(initial=True))
    uvicorn.run('app:app', host="0.0.0.0", workers=4, port=int(os.getenv('PORT', 8080)))
