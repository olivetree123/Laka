# Laka
[![Build Status](https://travis-ci.org/olivetree123/Laka.svg?branch=master)](https://travis-ci.org/olivetree123/Laka)  [![codecov](https://codecov.io/gh/olivetree123/Laka/branch/master/graph/badge.svg)](https://codecov.io/gh/olivetree123/Laka)  ![PyPI](https://img.shields.io/pypi/v/laka?color=blue)  [![codebeat badge](https://codebeat.co/badges/6952feeb-ed2b-4646-818c-e294dad5fe79)](https://codebeat.co/projects/github-com-olivetree123-laka-master)  ![PyPI - License](https://img.shields.io/pypi/l/laka)  

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
from laka import Laka, Param, Handler, HandlerFailed, HandlerOK
from laka.errors import ValidateError, HandlerNotFound, InvalidHandler, \
                        InvalidMessage, MakeCommandError, MakeResponseError



# 定义命令
COMMAND_CREATE_USER = 101

# 返回码定义
SUCCESS = 0                 # 成功
COMMAND_NOT_FOUND = 1       # 未找到命令
VALIDATE_PARAM_FAILED = 10  # 参数错误
INTERNAL_ERROR = 500        # 服务器内部错误

# 返回码对应的提示信息
RESPONSE_MESSAGE = {
    SUCCESS: "",
    COMMAND_NOT_FOUND: "Command not found.",
    VALIDATE_PARAM_FAILED: "Failed to validate params",
    INTERNAL_ERROR: "Internal Server Error",
}

HandlerOK.set_success_code(SUCCESS)


# 参数
class CreateUserParam(Param):
    
    def __init__(self):
        self.account = None
        self.password = None
        self.tel = None
    
    def validate(self):
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
    laka = Laka(redis_host="localhost", redis_port=6379, redis_queue="laka_request", response_message=RESPONSE_MESSAGE)
    try:
        # 注册路由
        laka.register(COMMAND_CREATE_USER, CreateUserHandler)
    except InvalidHandler as e:
        logging.error(e)
        sys.exit(1)
    try:
        # 开始监听请求
        for cmd in laka.accept_request():
            try:
                handler_response = laka.handle(cmd)
            except ValidateError as e:
                logging.error(e)
                handler_response = HandlerFailed(VALIDATE_PARAM_FAILED)
            except MakeHandlerResponseError as e:
                logging.error(e)
                handler_response = HandlerFailed(INTERNAL_ERROR)
            except HandlerNotFound as e:
                logging.error(e)
                handler_response = HandlerFailed(COMMAND_NOT_FOUND)
            try:
                laka.response(cmd.request_id, handler_response)
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
import logging
from laka import Laka, Param
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
    laka = Laka(redis_host="localhost", redis_port=6379, redis_queue="laka_request")
    param = CreateUserParam("olivetree", "123456")
    try:
        # 发送请求
        request_id = laka.request(COMMAND_CREATE_USER, param)
    except MakeCommandError as e:
        logging.error(e)
        sys.exit(1)
    except MakeRequestError as e:
        logging.error(e)
        sys.exit(1)
    try:
        # 获取结果，会阻塞等待
        response = laka.accept_response(request_id)
    except MakeResponseError as e:
        logging.error(e)
        sys.exit(1)
    logging.info(response.json())
```