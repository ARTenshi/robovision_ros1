#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>

#include <opencv2/highgui/highgui.hpp>

int main(int argc, char** argv)
{
	//Start your ROS node
	ROS_INFO("Starting image_publisher application...");
	ros::init(argc, argv, "image_publisher");

	//Create a handler for your ROS element
	ros::NodeHandle nh;
	image_transport::ImageTransport it(nh);
	image_transport::Publisher pub = it.advertise("camera/image", 1);

	//Read the input data
	cv::Mat image = cv::imread(argv[1], cv::IMREAD_COLOR);

	//Convert the output data into a ROS message format
	sensor_msgs::ImagePtr msg = cv_bridge::CvImage(std_msgs::Header(), "bgr8", image).toImageMsg();

	//Let's publish our images at a frequency of 30 frames per second
	ros::Rate rate(30);
	while (nh.ok())
	{
		//Publish your messages in your ROS topics
		pub.publish(msg);

		//Prepare ROS to publish the next message
		ros::spinOnce();
		rate.sleep();
	}
}

