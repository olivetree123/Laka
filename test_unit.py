import pytest
from .laka import LakaServer, LakaClient
from .laka.param import Param
from .laka.command import Command
from .laka.handler import Handler, HandlerOK


class CreateUserParam(Param):
    
    def __init__(self, account=None, password=None, tel=None):
        self.account = account
        self.password = password
        self.tel = tel
    
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


COMMAND_CREATE_USER = 100

cmd_dict = {
    "code": COMMAND_CREATE_USER,
    "request_id":"123",
    "params": {
        "account": "data1",
        "password": "data2",
    }
}

class TestCase(object):

    def setup_class(self):
        print("开始执行测试用例")
        self.create_server(self)
        self.create_client(self)
        
    def teardown_class(self):
        print("测试用例执行结束")
    
    def create_server(self):
        self.laka_server = LakaServer(
            service_name="lakaTest",
            redis_host="localhost", 
            redis_port=6379, 
            redis_queue="laka_request", 
            fofo_host="localhost",
            fofo_port=6379,
            check_health=False,
        )
        self.laka_server.router(COMMAND_CREATE_USER, CreateUserHandler)
        HandlerOK.set_success_code(0)
        self.cmd = None
    
    def create_client(self):
        self.laka_client = LakaClient(
            service_name="lakaTest",
            fofo_host="localhost",
            fofo_port=6379,
        )

    def setup(self):
        pass
        # print("setup：每个用例开始前都会执行")

    def teardown(self):
        pass
        # print("teardown：每个用例结束后都会执行")

    def test_request(self):
        param = CreateUserParam("olivetree", "123456")
        request_id = self.laka_client.request(COMMAND_CREATE_USER, param)
        data = self.laka_server._accept(self.laka_server.service.queue)
        self.cmd = Command.load_from_dict(data[1])
        result = self.laka_server.handle(self.cmd)
        self.laka_server.response(request_id, result)
        self.handle_response()
    
    def handle_response(self):
        resp = self.laka_client.accept_response(self.cmd.request_id)
        print(resp.json())


if __name__ == "__main__":
    pytest.main(["-s", "test_unit.py"])