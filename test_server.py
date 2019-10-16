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

