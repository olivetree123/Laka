import time
from laka.fofo import Fofo
from laka import LakaService


if __name__ == "__main__":
    fofo = Fofo("10.88.190.211", 6379)
    service = LakaService("service2", "localhost1", 6380, "queue1")
    service = fofo.register_service(service)
    print("service 111 = ", service)
    fofo.health_check()
    service = fofo.get_service(service["id"])
    print("service 222 = ", service)
    r = fofo.search_service(name="service2")
    print("r = ", r)
    fofo.heart_beat_thread.join()
    