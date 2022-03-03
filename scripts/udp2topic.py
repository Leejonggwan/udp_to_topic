#! /usr/bin/env python

import rospy
from std_msgs.msg import String
import socket

class U2T:
    def __init__(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.sock.bind(("", 4210))
        except socket.SO_ERROR as e:
            rospy.logerr(e)
            rospy.logerr("UDP Socket is not Connected")
            rospy.signal_shutdown()
        rospy.init_node("udp2topic")
        self.msg_pub = rospy.Publisher(
            "/traffic_flag",
            String,
            queue_size=3
        )

    def recv_msg(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            data = data.decode()
            if data == "":
                pass
            else:
                self.msg_pub.publish(data)

if __name__ == "__main__":
    u2t = U2T()
    u2t.recv_msg()