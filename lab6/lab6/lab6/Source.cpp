#pragma comment(lib, "wldap32.lib") 
#pragma comment(lib, "ws2_32.lib") 
#pragma comment(lib, "winmm.lib") 

#include <stdio.h>
#include "curl\curl.h"
#include <iostream>
#include "string.h"

#include <stdlib.h>
#include <sstream>


using namespace std;

int main(void)
{

	bool post = true;

	curl_global_init(CURL_GLOBAL_ALL);
	CURL * myHandle = curl_easy_init();

	CURLcode result;

	// Data to send
	string url = "http://52.37.129.225:443/signin";

	string postMessage = "";
	string name = "";
	string password = "";

		if (post)
		{
			cout << "Enter name: " << endl;
			cin >> name;
			cout << "Enter password: " << endl;
			cin >> password;

			postMessage = "name=Test&name=" + name + "&password=" + password;
		}

		// Sets URL
		curl_easy_setopt(myHandle, CURLOPT_URL, url.c_str());

		curl_easy_setopt(myHandle, CURLOPT_URL, url.c_str());
		if (post)
		{
			curl_easy_setopt(myHandle, CURLOPT_POSTFIELDS, postMessage.c_str());
		}
	
	// Will perform an action.
		result = curl_easy_perform(myHandle);

		// Will clean it, so it can be used again.
		curl_easy_cleanup(myHandle);

		std::cout << endl;
		std::cout << endl;
		std::cout << result;
		std::cout << endl;
		std::cout << endl;


	system("PAUSE");
	return 0;
	system("PAUSE");
	return 0;
}