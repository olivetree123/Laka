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
    param = CreateUserParam("olivetree123", "123456")
    try:
        request_id = laka.request(COMMAND_CREATE_USER, param)
    except MakeCommandError as e:
        logging.error(e)
        sys.exit(1)
    except MakeRequestError as e:
        logging.error(e)
        sys.exit(1)
    try:
        response = laka.accept_response(request_id)
    except MakeResponseError as e:
        logging.error(e)
        sys.exit(1)
    logging.info(response.json())
