# Laka

Laka 是为 Python 打造的基于 json 和 redis 的微服务框架。

## Tutorial

Server 端:
``` python
import logging
from laka import Laka, Param
from laka.response import Response, INVALID_PARAM, COMMAND_NOT_FOUND


class CreateUserParam(Param):
    CommandCode = 101
    
    def __init__(self):
        self.account = None
        self.username = None
    
    def validate(self):
        if not self.username:
            return False
        return True


def create_user(cmd):
    try:
        param = CreateUserParam.load_from_cmd(cmd)
    except Exception as e:
        logging.error(e)
        return None, INVALID_PARAM
    user = {"username":param.username, "account":param.account}
    return user, 0
    

if __name__ == "__main__":
    laka = Laka(redis_host="localhost", redis_port=6379)
    for cmd in laka.accept_request():
        data, resp_code = None, COMMAND_NOT_FOUND
        if cmd.code == CreateUserParam.CommandCode:
            data, resp_code = create_user(cmd)
        laka.response(cmd.request_id, resp_code, data)

```


Client 端:
``` python
from laka import Laka


CREATE_USER_COMMAND = 101

if __name__ == "__main__":
    laka = Laka(redis_host="localhost", redis_port=6379)
    request_id = laka.send(CREATE_USER_COMMAND, {"username":"olivetree"})
    response = laka.accept_response(request_id)
    print(response.json())
```