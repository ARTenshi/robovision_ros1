#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <opencv2/highgui/highgui.hpp>
#include <cv_bridge/cv_bridge.h>

int main(int argc, char** argv)
{
	//Start your ROS node
	ROS_INFO("Starting image_publisher application...");
	ros::init(argc, argv, "image_publisher");

	//Create a handler for your ROS element
	ros::NodeHandle nh;
	image_transport::ImageTransport it(nh);
	image_transport::Publisher pub = it.advertise("camera/image", 1);

	//Select a camera source (0, 1, 2...)
	int video_source = 0;

	//Open the seleted camera
	cv::VideoCapture cap(video_source);

	// Check if the camera is working
	if(!cap.isOpened()) return 1;

	//Start your frames and ROS messages to be published
	cv::Mat frame;
	sensor_msgs::ImagePtr msg;

	//Let's publish our images at a frequency of 30 frames per second
	ros::Rate loop_rate(30);
	while (nh.ok())
	{
		//Grab a new frame
		cap >> frame;

		// Check if the captured frame has some content
		if(!frame.empty())
		{
			//Convert the output data into a ROS message format
			msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", frame).toImageMsg();

			//Publish your messages to your ROS topics
			pub.publish(msg);
		}

		//Prepare ROS to publish the next message
		ros::spinOnce();
		loop_rate.sleep();
  	}
}
