// rostime.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <iostream>
#include <sstream>
#include <ros/time.h>


//int _tmain(int argc, char** argv)
int _tmain(int argc, _TCHAR* argv[])
{

	ros::Time::init();
	ros::Time time;

	std::cout << "[" << time.now() << "] Hello Dude" << std::endl;
    std::cout << "[" << time.now() << "] Enter 'q' to quit" << std::endl;
	char c;
	std::cin >> c;
	return 0;
}

