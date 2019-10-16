# Laka
[![Build Status](https://travis-ci.org/olivetree123/Laka.svg?branch=master)](https://travis-ci.org/olivetree123/Laka)  [![codecov](https://codecov.io/gh/olivetree123/Laka/branch/master/graph/badge.svg)](https://codecov.io/gh/olivetree123/Laka)  [![Codacy Badge](https://api.codacy.com/project/badge/Grade/27a69db7d26b4642b77f292711c35022)](https://www.codacy.com/manual/olivetree123/Laka?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=olivetree123/Laka&amp;utm_campaign=Badge_Grade)  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/laka)  ![PyPI](https://img.shields.io/pypi/v/laka?color=blue)  ![PyPI - License](https://img.shields.io/pypi/l/laka)  

Laka is a microservice framework for Python, based on json and redis.

## Install
``` shell
pip install laka
```

## Tutorial

Server 端:
``` python
import sys
import logging
from laka import LakaServer, Param, Handler, HandlerFailed, HandlerOK
from laka.errors import ValidateError, HandlerNotFound, InvalidHandler, \
                        InvalidMessage, MakeCommandError, MakeResponseError, MakeHandlerResponseError


# 定义命令
COMMAND_CREATE_USER = 101

# 返回码定义
SUCCESS = 0                 # 成功
COMMAND_NOT_FOUND = 1       # 未找到命令
VALIDATE_PARAM_FAILED = 10  # 参数错误
INTERNAL_SERVER_ERROR = 500        # 服务器内部错误

# 返回码对应的提示信息
RESPONSE_MESSAGE = {
    SUCCESS: "",
    COMMAND_NOT_FOUND: "Command not found.",
    VALIDATE_PARAM_FAILED: "Failed to validate params",
    INTERNAL_SERVER_ERROR: "Internal Server Error",
}

HandlerOK.set_success_code(SUCCESS)


# 参数
class CreateUserParam(Param):
    
    def __init__(self):
        self.account = None
        self.password = None
        self.tel = None
    
    def validate(self):
        """
        接收到消息之后，会自动调用 validate 验证参数是否合法
        """
        if not (self.account and self.password):
            return False
        return True


# handler，用来处理请求
class CreateUserHandler(Handler):
    Param = CreateUserParam

    def handle(self):
        user = {"password":self.param.password, "account":self.param.account}
        return HandlerOK(user)
    

if __name__ == "__main__":
    laka_server = LakaServer(
        service_name="lakaTest",
        redis_host="localhost", 
        redis_port=6379, 
        redis_queue="laka_request", 
        consul_host="localhost",
        consul_port=8500,
        response_message=RESPONSE_MESSAGE,
    )
    try:
        laka_server.router(COMMAND_CREATE_USER, CreateUserHandler)
    except InvalidHandler as e:
        logging.error(e)
        sys.exit(1)
    try:
        for cmd in laka_server.accept_request():
            try:
                print("cmd = ", cmd.json())
                handler_response = laka_server.handle(cmd)
            except ValidateError as e:
                logging.error(e)
                handler_response = HandlerFailed(VALIDATE_PARAM_FAILED)
            except MakeHandlerResponseError as e:
                logging.error(e)
                handler_response = HandlerFailed(INTERNAL_SERVER_ERROR)
            except HandlerNotFound as e:
                logging.error(e)
                handler_response = HandlerFailed(COMMAND_NOT_FOUND)
            try:
                laka_server.response(cmd.request_id, handler_response)
            except MakeResponseError as e:
                logging.error(e)
                break
    except MakeCommandError as e:
        logging.error(e)
    except InvalidMessage as e:
        logging.error(e)
```


Client 端:
``` python
import sys
from laka import LakaClient, Param
from laka.errors import MakeResponseError, MakeRequestError, MakeCommandError


COMMAND_CREATE_USER = 101


class CreateUserParam(Param):
    
    def __init__(self, account, password, tel=None):
        self.account = account
        self.password = password
        self.tel = tel
    
    def validate(self):
        """
        发送请求之前，validate 会被自动调用
        """
        if not (self.account and self.password):
            return False
        return True


if __name__ == "__main__":
    laka_client = LakaClient(
        service_name="lakaTest",
        consul_host="localhost",
        consul_port=8500,
    )
    param = CreateUserParam("olivetree123", "123456")
    try:
        request_id = laka_client.request(COMMAND_CREATE_USER, param)
    except MakeCommandError as e:
        print(e)
        sys.exit(1)
    except MakeRequestError as e:
        print(e)
        sys.exit(1)
    try:
        response = laka_client.accept_response(request_id)
    except MakeResponseError as e:
        print(e)
        sys.exit(1)
    print("response = ", response.json())
```