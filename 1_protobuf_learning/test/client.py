# -*- coding: utf-8 -*-
"""
@Time: 2020/12/9 22:53 
@Author: Hudaiguo
@python version: 3.5.2
"""


import grpc
import hello_pb2 as pb2
import hello_pb2_grpc as pb2_grpc

def run():
    conn = grpc.insecure_channel("127.0.0.1:5000")
    client = pb2_grpc.Say_helloStub(channel=conn)
    resposne = client.hello_hu(pb2.hello_hu_request(name="hudaiguo",
                                       age=28))
    print(resposne.result)

if __name__ == "__main__":
    run()