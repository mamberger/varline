from uvicorn.workers import UvicornWorker


class UvicornCustomWorker(UvicornWorker):
    """
    этот класс нужно копировать и вставить в /usr/local/lib/python3.8/dist-packages/uvicorn/workers.py
    чтобы заработало нужно установить библиотеки
    pip install uvloop, httptools
    """
    CONFIG_KWARGS = {
        'loop': 'uvloop',
        'lifespan': 'on',
        "http": "httptools"
    }
