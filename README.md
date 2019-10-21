# Laka
[![Build Status](https://travis-ci.org/olivetree123/Laka.svg?branch=master)](https://travis-ci.org/olivetree123/Laka)  [![codecov](https://codecov.io/gh/olivetree123/Laka/branch/master/graph/badge.svg)](https://codecov.io/gh/olivetree123/Laka)  [![Codacy Badge](https://api.codacy.com/project/badge/Grade/27a69db7d26b4642b77f292711c35022)](https://www.codacy.com/manual/olivetree123/Laka?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=olivetree123/Laka&amp;utm_campaign=Badge_Grade)  ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/laka)  ![PyPI](https://img.shields.io/pypi/v/laka?color=blue)  ![PyPI - License](https://img.shields.io/pypi/l/laka)  

Laka is a microservice framework for Python, based on json and redis.

## Install
1. Step one
Install Fofo
2. Step two
    ``` shell
    pip install laka
    ```

## Feature
  - Service Register and Discovery
  - Transmit data with Json RPC

## Tutorial: Server
1. Create Server and Register Service
    ``` python
    from laka import LakaServer

    laka_server = LakaServer(
        service_name="lakaTest",    # Register Service with this name
        redis_host="localhost", 
        redis_port=6379, 
        redis_queue="laka_request", 
        fofo_host="10.88.190.211",
        fofo_port=6379,
        response_message=RESPONSE_MESSAGE,
        check_health=True,
    )
    ```
2. Define param for Handler
    ``` python
    from laka import Param

    class CreateUserParam(Param):
        def __init__(self):
            self.account = None
            self.password = None
            self.tel = None
        
        def validate(self):
            """
            validate will be run automatically
            you should not run validate by yourself
            """
            if not (self.account and self.password):
                return False
            return True
    ```
3. Define Handler
    ``` python
    from laka import Handler

    class CreateUserHandler(Handler):
        Param = CreateUserParam

        def handle(self):
            user = {"password":self.param.password, "account":self.param.account}
            return HandlerOK(user)
    ```
4. Add router
    ``` python
    # COMMAND_CREATE_USER = 101
    laka_server.router(COMMAND_CREATE_USER, CreateUserHandler)
    ```
5. Accept & Handle request 
    ``` python
    for queue, cmd in laka_server.accept_request():
        handler_response = laka_server.handle(cmd)
    ```
## Tutorial: Client
1. Create Client
    ``` python
    from laka import LakaClient

    laka_client = LakaClient(
        service_name="lakaTest",    # service_name is the service you want to connect to
        fofo_host="10.88.190.211",
        fofo_port=6379,
    )
    ```
2. Define & Create param 
    ``` python
    from laka import Param

    class CreateUserParam(Param):
        
        def __init__(self, account, password, tel=None):
            self.account = account
            self.password = password
            self.tel = tel
        
        def validate(self):
            """
            validate will be run in request automatically
            you should not run validate by yourself
            """
            if not (self.account and self.password):
                return False
            return True

    param = CreateUserParam("olivetree", "123456")
    ```
3. Send Request
    ``` python
    request_id = laka_client.request(COMMAND_CREATE_USER, param)
    ```
4. Get Response
    ``` python
    response = laka_client.accept_response(request_id)
    print("response = ", response.json())
    ```