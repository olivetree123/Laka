import pytest
from .laka.laka import Laka
from .laka.param import Param
from .laka.command import Command
from .laka.handler import Handler, HandlerOK


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


CREATE_USER_COMMAND = 100

cmd_dict = {
    "code": CREATE_USER_COMMAND,
    "request_id":"123",
    "params": {
        "account": "data1",
        "password": "data2",
    }
}

class TestCase(object):

    def setup_class(self):
        print("开始执行测试用例")
        self.laka = Laka(redis_host="localhost", redis_port=6379, redis_queue="laka_request")
        self.laka.register(CREATE_USER_COMMAND, CreateUserHandler)
        HandlerOK.set_success_code(0)
        self.cmd = None

    def teardown_class(self):
        print("测试用例执行结束")

    def setup(self):
        pass
        # print("setup：每个用例开始前都会执行")

    def teardown(self):
        pass
        # print("teardown：每个用例结束后都会执行")

    def test_request(self):
        self.cmd = Command.load_from_dict(cmd_dict)
        result = self.laka.handle(self.cmd)
        self.laka.response(self.cmd.request_id, result)
        self.response()
    
    def response(self):
        resp = self.laka.accept_response(self.cmd.request_id)
        print(resp.json())


    # def test_param(self):

if __name__ == "__main__":
    pytest.main(["-s", "test_unit.py"])