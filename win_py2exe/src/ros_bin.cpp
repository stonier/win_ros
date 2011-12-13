/**
 * @file /src/ros_bin.cpp
 *
 * @brief Self describing executable for launching python scripts in ${ROS_ROOT}/bin
 *
 * @date March 2011
 **/

/*****************************************************************************
** Includes
*****************************************************************************/

#include <iostream>
#include <cstdlib>
#include <sstream>
#include <algorithm>
#ifdef WIN32
  #include <windows.h>
#endif

char name[256];
std::string ros_root, python_home, python_file, python_exe;
std::stringstream arguments;

/*****************************************************************************
** Functions
*****************************************************************************/

void print_environment_variables() {
	std::cout << "Environment Variables:" << std::endl;
	std::cout << "  PYTHONHOME: " << python_home << std::endl;
	std::cout << "  ROS_ROOT: " << ros_root << std::endl;
	std::cout << std::endl;
}

void debug() {
	print_environment_variables();
	std::cout << std::endl;
	std::cout << "Program Variables:" << std::endl;
	std::cout << "  Python exe: " << python_exe << std::endl;
	std::cout << "  Target name: " << name << std::endl;
	std::cout << "  Target python file: " << python_file << std::endl;
	std::cout << "  Arguments: " << arguments.str() << std::endl;
	std::cout << std::endl;
}


/*****************************************************************************
** Main
*****************************************************************************/

int main(int argc, char **argv) {

	name[0] = '\0';
#ifdef WIN32
	_splitpath(argv[0], NULL, NULL, name, NULL);
//	for ( int i = 0; i < argc; ++i ) {
//		std::cout << "Argument[" << i << "] " << argv[i] << std::endl;
//	}

	ros_root = std::getenv("ROS_ROOT");
	python_home = std::getenv("PYTHONHOME");
	std::transform(python_home.begin(), python_home.end(), python_home.begin(), ::tolower);
	std::string::iterator iter;
	for ( iter = python_home.begin(); iter < python_home.end(); ++iter ) {
		if ( *iter == '\\' ) {
			*iter = '/';
		}
	}

	python_file = ros_root+std::string("/bin/")+std::string(name);
	python_exe = python_home + std::string("/python.exe");
	arguments << " " << python_file;
	for ( int i = 1; i < argc; ++i ) {
		// need the quotes to make sure spaces dont muck things up
		arguments << " \"" << argv[i] << "\"";
	}

	/* TODO: Need some validation checks here! */


	STARTUPINFO startup_info;
	PROCESS_INFORMATION process_info;
	memset(&startup_info, 0, sizeof(startup_info));
	memset(&process_info, 0, sizeof(process_info));

	startup_info.cb = sizeof(startup_info);

	int result =
		CreateProcess(
			python_exe.c_str(),
			const_cast<char*>(arguments.str().c_str()), // bloody windoze
			NULL,
			NULL,
			FALSE,
			0, // CREATE_NEW_CONSOLE,
			NULL,
			NULL,
			&startup_info,
			&process_info
			);
	if ( result == 0 ) {
		switch ( result ) {
			case ( ERROR_FILE_NOT_FOUND ) : {
				std::cout << "The python executable could not be found - check PYTHONHOME has been correctly set in winsetup.py" << std::endl;
				debug();
				break;
			}
			default: {
				std::cout << "Process failed with error: " << GetLastError() << std::endl;
				debug();
				break;
			}
		}
	} else {
		WaitForSingleObject( process_info.hProcess, INFINITE );
	    CloseHandle( process_info.hProcess );
	    CloseHandle( process_info.hThread );
	}
#else
	std::cout << "This is a windows application only." << std::endl;
	// No implementation yet
#endif
	return 0;
}




