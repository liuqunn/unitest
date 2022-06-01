"""
    示例pytest
"""

from proto import user_v1_user_pb2, user_v1_user_pb2_grpc
import grpc

# def run():
#     print("aaa")
#     channel = grpc.insecure_channel("127.0.0.1:9000")
#     stub = agh_pb2_grpc.AghStub(channel)
#     response = stub.GetViewerInfo(agh_pb2.GetViewerInfoReq(user_id="123"))
#     print(response.code, response.message)
#     print("bbb")


channel = grpc.insecure_channel("121.41.212.143:8180")


def ping():
    print("into ping...")
    stub = user_v1_user_pb2_grpc.interfaceStub(channel)
    response = stub.Ping(user_v1_user_pb2.PingReq())
    print(response.Now)
    print("outgoing ping...")


def video_wall_page():
    print("into VideoWallPage...")
    data = {"token": "750.chb7z07mf6pt1g0o76t3bwz59bhv79jm", "channel": "1", "campaignname": "other"}
    stub = user_v1_user_pb2_grpc.interfaceStub(channel)
    print(tuple(data.items()))
    response, call = stub.VideoWallPage.with_call(request=user_v1_user_pb2.VideoWallReq(page=1, pageLimit=10),
                                                  metadata=tuple(data.items()))
    print(response)
    # video_walls = response.wall
    # for i in video_walls:
    #     assert i.Id == 1
    print("outgoing VideoWallPage...")


def discovery_page():
    print("into discovery_page...")
    header = {"token": "710.chb6ghuvwbcg1c0kazw0vgl3rqdo76vn", "channel": "1"}
    stub = user_v1_user_pb2_grpc.interfaceStub(channel)
    response, call = stub.DiscoverPage.with_call(request=user_v1_user_pb2.DiscoverReq(page=1, pageLimit=2),
                                                 metadata=tuple(header.items()))
    print(response)
    print("outgoing discovery_page...")


def init_req():
    print("into init_req...")
    stub = user_v1_user_pb2_grpc.interfaceStub(channel)
    response, call = stub.AppInit.with_call(request=user_v1_user_pb2.InitReq(campaignName="xiaomi"))
    print(response)
    print("outgoing init_req...")


def guest_login():
    print("into guest_login...")
    stub = user_v1_user_pb2_grpc.interfaceStub(channel)
    response, call = stub.UserGuestLogin.with_call(request=user_v1_user_pb2.UserGuestLoginReq(deviceId="wrx"))
    print(response)
    print("outgoing guest_login...")


# guest_login()
video_wall_page()
