#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from sensor_msgs.msg import Image, PointCloud2
import cv2
from cv_bridge import CvBridge
import ros_numpy
import numpy as np
import traceback
import tf

global rgb_mat
global depth_mat, depth_img
global object_centroid

global display

rgb_mat=0
depth_mat=0
depth_img=0
object_centroid=Pose()

display =True

def callback_rgb_rect(msg):
	global rgb_mat

	try:
		bridge_rgb=CvBridge()
		rgb_mat=bridge_rgb.imgmsg_to_cv2(msg,"bgr8").copy()
	except:
		rospy.logerr(traceback.format_exc())

def callback_depth_rect(msg):
	global depth_mat, depth_img
	global display

	try:
		display=True
		bridge_depth=CvBridge()
		depth_img=bridge_depth.imgmsg_to_cv2(msg,"32FC1").copy()

		depth_mat = np.array(depth_img, dtype=np.float32)
		cv2.normalize(depth_mat, depth_img, 0, 1, cv2.NORM_MINMAX)
	except:
		rospy.logerr(traceback.format_exc())

def callback_point_cloud(msg):
	global object_centroid

	try:
		#Transform the ROS Point Cloud message to a Python array
		pc = ros_numpy.numpify(msg)

		rows, cols = pc.shape
		print ('point cloud size: rows: {}, cols: {}'.format(rows, cols))

		#Access a point in the point_cloud
		row_id = rows/2 
		col_id = cols/2 

		p = [pc[row_id][col_id][0], pc[row_id][col_id][1], pc[row_id][col_id][2]]

		object_centroid.position.x = p[0]
		object_centroid.position.y = p[1]
		object_centroid.position.z = p[2]

		object_centroid.orientation.x=0
		object_centroid.orientation.y=0
		object_centroid.orientation.z=0
		object_centroid.orientation.w=0

		print ('central point: {}'.format(p))
	except:
		rospy.logerr(traceback.format_exc())

def main():
	global rgb_mat
	global depth_mat, depth_img
	global display

	#Start your ROS node
	print "Initializing rgbd_reader"
	rospy.init_node('rgbd_reader', anonymous=True)

	#Subscribers (sources)
	rospy.Subscriber("/camera/rgb/image_rect_color", Image , callback_rgb_rect)
	rospy.Subscriber("/camera/depth_registered/image", Image, callback_depth_rect)
	rospy.Subscriber("/camera/depth_registered/points", PointCloud2, callback_point_cloud)

	#Publishers (results)
	pub_centroid=rospy.Publisher('/object_centroid', Pose, queue_size=1)

	#Initialising object_centroid variable
	global object_centroid

	object_centroid.position.x=0
	object_centroid.position.y=0
	object_centroid.position.z=0
	object_centroid.orientation.x=0
	object_centroid.orientation.y=0
	object_centroid.orientation.z=0
	object_centroid.orientation.w=0

	#Main loop
	loop=rospy.Rate(10)
	while not rospy.is_shutdown():

		if(display):
			cv2.imshow("rgb", rgb_mat)
			cv2.imshow("depth", depth_img)
			cv2.waitKey(1)

		#Publishing to the /object_centroid topic
		#In this example, the ROS publisher "object_centroid" is updated in the 
		#callback_point_cloud function
		pub_centroid.publish(object_centroid)
		loop.sleep()


if __name__=='__main__':
	try:
		main()
		cv2.destroyAllWindows()
	except rospy.ROSInterruptException:
		pass
