if __name__ == "__main__":
    import uvicorn
    import sys
    import os

    sys.path.append(os.getcwd() + '/app')
    # uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run("app.main:app", host="0.0.0.0", port=30005, reload=True)
