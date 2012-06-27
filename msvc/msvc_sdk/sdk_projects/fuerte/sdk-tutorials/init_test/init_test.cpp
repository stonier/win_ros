// init_test.cpp : Defines the entry point for the console application.
//
#include "stdafx.h"
#include <string>
//#include <iostream>
//#include <sstream>
#include <ros/ros.h>
//#include <std_msgs/String.h>

//typedef std::basic_string<TCHAR> tstring; 

//int _tmain(int argc, _TCHAR* argv[])
int _tmain(int argc, char** argv)
{
	//std::string name("talker");
	std::string name2 = "talker";
	//const char name[10] = "talker";
	//wchar_t wArr[] = L"talker";
	//int  wLen;
	//char *cArr;
 	//wLen = wcslen(wArr);
	//////cArr = (char*)calloc( 1, wLen*2+1);
	//WideCharToMultiByte(CP_ACP,0, wArr, wLen, cArr, wLen*2,0,0);
 	//std::string str = cArr;

	ros::init(argc, argv, name2, 0);
	
	return 0;
}
