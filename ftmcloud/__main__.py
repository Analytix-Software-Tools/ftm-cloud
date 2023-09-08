import os

import uvicorn

if __name__ == '__main__':
    uvicorn.run('app:app', host="0.0.0.0", workers=4, port=int(os.getenv('PORT', 8080)), reload=True)
