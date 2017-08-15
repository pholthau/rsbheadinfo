#!/usr/bin/env python

import logging

import rospy
from std_msgs.msg import String
from people_msgs.msg import Person
from people_msgs.msg import People

import rsb
import rst
import rstsandbox

from rst.vision.HeadObject_pb2 import HeadObject
from rsb.converter import ProtocolBufferConverter, registerGlobalConverter

def convert(rosdata):

    person_msg = rosdata.people[0]

    headobj = HeadObject()

    #head bounding box (required)
    headobj.region.top_left.x = 1
    headobj.region.top_left.y = 2
    headobj.region.width = 3
    headobj.region.height = 4

    #head pan/tilt (required)
    headobj.pose.x = 5
    headobj.pose.y = 6
    headobj.pose.z = 0

    #optional
    personinfo = person_msg.name
    #gender:age
    headobj.position.x = person_msg.position.x
    headobj.position.y = person_msg.position.y
    headobj.position.z = person_msg.position.z

    return headobj

def publish(rstdata):
    informer.publishData(rstdata)

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + ' Received %s', data.data)
    rstdata = convert(data.data)
    publish(rstdata)


def ros_listen():
    rospy.init_node('poselistener', anonymous=True)
    rospy.Subscriber('/clf_detect_dlib_faces/people', People, callback)
    rospy.spin()

if __name__ == '__main__':

    logging.basicConfig()

    rsb.converter.registerGlobalConverter(rsb.converter.ProtocolBufferConverter(messageClass=HeadObject))
    with rsb.createInformer("/pepper/headpose", dataType=HeadObject) as informer:
        ros_listen()
