import sys
import logging
from laka import Laka, Param, Handler, HandlerFailed, HandlerOK
from laka.errors import ValidateParamsFailedError, HandlerNotFound, InvalidHandler, \
                        InvalidMessage, MakeCommandError, MakeResponseError



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
    CommandCode = 101
    Param = CreateUserParam

    def handle(self):
        user = {"password":self.param.password, "account":self.param.account}
        return HandlerOK(user)
    

if __name__ == "__main__":
    laka = Laka(redis_host="localhost", redis_port=6379, redis_queue="laka_request", response_message=RESPONSE_MESSAGE)
    try:
        laka.register(CreateUserHandler)
    except InvalidHandler as e:
        logging.error(e)
        sys.exit(1)
    try:
        for cmd in laka.accept_request():
            try:
                handler_response = laka.handle(cmd)
            except ValidateParamsFailedError as e:
                logging.error(e)
                handler_response = HandlerFailed(VALIDATE_PARAM_FAILED)
            except ResponseTypeError as e:
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

