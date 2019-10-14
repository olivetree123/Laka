from laka import Laka
from laka.errors import MakeResponseError


CREATE_USER_COMMAND = 101

if __name__ == "__main__":
    laka = Laka(redis_host="localhost", redis_port=6379, redis_queue="laka_request")
    request_id = laka.request(CREATE_USER_COMMAND, {"username":"olivetree"})
    try:
        response = laka.accept_response(request_id)
    except MakeResponseError as e:
        print(e)
        exit(1)
    print(response.json())
