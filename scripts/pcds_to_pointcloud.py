#!/usr/bin/env python

import rospy
import os
import sensor_msgs.msg
from std_msgs.msg import String
from sensor_msgs.msg import PointCloud2
import numpy as np
import pypcd

pcd_data_dir = "/home/asimo/rnd/data/jlr_pcd_data/pcd2"

def talker():
    pcd_files = sorted(os.listdir(pcd_data_dir))
    pub = rospy.Publisher('/velodyne_points', PointCloud2, queue_size=10)
    rospy.init_node('pcds_to_pointcloud', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    count = 0
    while not rospy.is_shutdown() and count < len(pcd_files):
        pcl_data = pypcd.PointCloud.from_path(os.path.join(pcd_data_dir, pcd_files[count]))
        outmsg = pcl_data.to_msg()
        outmsg.header.stamp = rospy.Time(count * 0.1000000000)
        outmsg.header.frame_id = "velodyne"
        count = count + 1
        rospy.loginfo(str(count)) 
        pub.publish(outmsg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

