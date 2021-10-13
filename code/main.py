import multiprocessing
from boot import init


app = init()


if __name__ == "__main__":
    cpu_count = multiprocessing.cpu_count()
    app.run("0.0.0.0", 80, workers=cpu_count, access_log=False)
