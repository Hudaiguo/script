# -*- coding: utf-8 -*-
"""
@Time: 2020/12/9 22:24 
@Author: Hudaiguo
@python version: 3.5.2
"""

import time
import grpc
import hello_pb2 as pb2
import hello_pb2_grpc as pb2_grpc
from concurrent import futures

class Bilibili(pb2_grpc.Say_helloServicer):
    def hello_hu(self, request, context):
        name = request.name
        age = request.age

        result = "my name is {}, I am {} years old.".format(name, age)
        return pb2.hello_hu_reply(result=result)

def run():
    grpc_serve = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4))
    pb2_grpc.add_Say_helloServicer_to_server(Bilibili(), grpc_serve)
    grpc_serve.add_insecure_port("127.0.0.1:5000")
    print("server will start at 127.0.0.1:5000")
    grpc_serve.start()

    try:
        while(1):
            time.sleep(3600)
    except KeyboardInterrupt:
        grpc_serve.start(0)


if __name__ == "__main__":
    run()