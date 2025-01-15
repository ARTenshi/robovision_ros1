#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>

#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <string>

bool display = true;

void callback_image(const sensor_msgs::ImageConstPtr& msg)
{
	try
	{
		//Transform the new message to an OpenCV matrix
		cv::Mat img;
		img = cv_bridge::toCvShare(msg, "bgr8")->image.clone();

		//Show your images
		if (display)
		{
			cv::imshow("view", img);
			cv::waitKey(30);
		}
	}
	catch (cv_bridge::Exception& e)
	{
		//In case of error, report it
		ROS_ERROR("Could not convert from '%s' to 'bgr8'.", msg->encoding.c_str());
	}

}

int main(int argc, char **argv)
{
	//Start your ROS node
	ROS_INFO("Starting image_listener application in c++...");
	ros::init(argc, argv, "image_listener");

	//Create a handler for your ROS element
  	ros::NodeHandle nh;
	image_transport::ImageTransport it(nh);
	//Tell ROS what to do when a new message (Image) arrives!
	//ROS will execute the commands in the callback function
	image_transport::Subscriber sub = it.subscribe("camera/image", 1, callback_image);

	//Start an infinite loop in ROS
	ros::spin();

	//Destroy any opened OpenCV window before finishing 
	cv::destroyWindow("view");
}
