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
        fofo_host="10.88.190.211",
        fofo_port=6379,
    )
    param = CreateUserParam("olivetree", "123456")
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
