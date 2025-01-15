#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
import numpy as np
import traceback
import tf

#Declare your global variables
global img, is_img, display

img=[]
is_img = False

display = True

def callback_image(msg):
	global img, is_img

	try:
		#Transform the new message to an OpenCV matrix
		bridge_rgb=CvBridge()
		img = bridge_rgb.imgmsg_to_cv2(msg,msg.encoding).copy()
		is_img = True
	except:
		rospy.logerr(traceback.format_exc())

def main():
	#Start your ROS node
	rospy.loginfo('Starting image_listener application in python...')
	rospy.init_node('image_listener', anonymous=True)

	#Tell ROS what to do when a new message (Image) arrives!
	#ROS will execute the commands in the callback functions
	rospy.Subscriber("camera/image", Image , callback_image)

	global img, is_img, display

	loop=rospy.Rate(30)
	while not rospy.is_shutdown():
		if is_img:
			#Show your images
			if(display):
				cv2.imshow("view", img)
				cv2.waitKey(1)

			loop.sleep()

if __name__=='__main__':
	try:
		main()
		cv2.destroyAllWindows()
	except rospy.ROSInterruptException:
		pass
