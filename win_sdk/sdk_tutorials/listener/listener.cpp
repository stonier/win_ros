// listener.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <map>
#include <ros/ros.h>
#include <std_msgs/String.h>

#include <sstream>

/**
 * This tutorial demonstrates simple receipt of messages over the ROS system.
 */

void chatterCallback(const std_msgs::String::ConstPtr& msg)
{
	ROS_INFO("I heard: [%s]", msg->data.c_str());
}

int _tmain(int argc, char** argv)
{
	/**
	* If you want to use environment variables, that also works in windows.
	*/
	ros::init(argc, argv, "win_listener");

	/**
	* However its often easier to pick up those parameters from elsewhere 
	* (file, ui, ...) as win-ros doesn't have the complete infrastructure
	* for things like roslaunch yet.
	*/
    // std::map<std::string,std::string> remappings;
	// remappings["__master"] = "http://192.168.10.161:11311";
	// remappings["__hostname"] = "192.168.10.66";
	// ros::init(remappings,"win_listener");

	/**
	* NodeHandle is the main access point to communications with the ROS system.
	* The first NodeHandle constructed will fully initialize this node, and the last
	* NodeHandle destructed will close down the node.
	*/
	ros::NodeHandle n;

	/**
	* The subscribe() call is how you tell ROS that you want to receive messages
	* on a given topic.  This invokes a call to the ROS
	* master node, which keeps a registry of who is publishing and who
	* is subscribing.  Messages are passed to a callback function, here
	* called chatterCallback.  subscribe() returns a Subscriber object that you
	* must hold on to until you want to unsubscribe.  When all copies of the Subscriber
	* object go out of scope, this callback will automatically be unsubscribed from
	* this topic.
	*
	* The second parameter to the subscribe() function is the size of the message
	* queue.  If messages are arriving faster than they are being processed, this
	* is the number of messages that will be buffered up before beginning to throw
	* away the oldest ones.
	*/
	ros::Subscriber sub = n.subscribe("chatter", 1000, chatterCallback);

	/**
	* ros::spin() will enter a loop, pumping callbacks.  With this version, all
	* callbacks will be called from within this thread (the main one).  ros::spin()
	* will exit when Ctrl-C is pressed, or the node is shutdown by the master.
	*/
	ros::spin();

	return 0;
}
