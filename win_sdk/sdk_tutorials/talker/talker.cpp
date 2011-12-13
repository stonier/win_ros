// talker.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <ros/ros.h>
#include <std_msgs/String.h>

#include <sstream>

int _tmain(int argc, char** argv)
{
	/**
	* If you want to use environment variables, that also works in windows.
	*/
	ros::init(argc, argv, "win_talker");

	/**
	* However its often easier to pick up those parameters from elsewhere 
	* (file, ui, ...) as win-ros doesn't have the complete infrastructure
	* for things like roslaunch yet.
	*/
    // std::map<std::string,std::string> remappings;
	// remappings["__master"] = "http://192.168.10.161:11311";
	// remappings["__hostname"] = "192.168.10.66";
	// ros::init(remappings,"win_talker");

  /**
   * NodeHandle is the main access point to communications with the ROS system.
   * The first NodeHandle constructed will fully initialize this node, and the last
   * NodeHandle destructed will close down the node.
   */
  ros::NodeHandle n;

  /**
   * The advertise() function is how you tell ROS that you want to
   * publish on a given topic name. This invokes a call to the ROS
   * master node, which keeps a registry of who is publishing and who
   * is subscribing. After this advertise() call is made, the master
   * node will notify anyone who is trying to subscribe to this topic name,
   * and they will in turn negotiate a peer-to-peer connection with this
   * node.  advertise() returns a Publisher object which allows you to
   * publish messages on that topic through a call to publish().  Once
   * all copies of the returned Publisher object are destroyed, the topic
   * will be automatically unadvertised.
   *
   * The second parameter to advertise() is the size of the message queue
   * used for publishing messages.  If messages are published more quickly
   * than we can send them, the number here specifies how many messages to
   * buffer up before throwing some away.
   */
  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
  ros::Rate loop_rate(10);

  /**
   * A count of how many messages we have sent. This is used to create
   * a unique string for each message.
   */
  int count = 0;
  while (ros::ok())
  {
    /**
     * This is a message object. You stuff it with data, and then publish it.
     */
    std_msgs::String msg;

    std::stringstream ss;
    ss << "hello world " << count;
    msg.data = ss.str();

    ROS_INFO("%s", msg.data.c_str());

    /**
     * The publish() function is how you send messages. The parameter
     * is the message object. The type of this object must agree with the type
     * given as a template parameter to the advertise<>() call, as was done
     * in the constructor above.
     */
    chatter_pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


	std::cout << "Enter 'q' to quit" << std::endl;
	char c;
	std::cin >> c;
	return 0;
}

