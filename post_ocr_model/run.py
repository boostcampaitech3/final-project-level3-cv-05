import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='localhost',
        port=8001,
        reload=True
    )
