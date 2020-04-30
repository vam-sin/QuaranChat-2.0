# Networks Assignment 3

Creating a reliable UDP protocol. This README explains what each of the files are. The project was implemented in Python. The problem statement can be found in the PDF file, `assignment-3.pdf`. We implemented a stop-and-go protocol to ensure reliability. 

1. `reliable_socket.py` contains the classes for our reliable UDP message and Reliable UDP socket. The reliable UDP socket implements high level functions send(), receive() and bind() so the end programmer need not concern himself with the inner workings.  
2. `UDP_C.py` and `UDP_S.py` are the toy server-client chat application. The file 
3. The folder `test_data` contains the random data used to test the file transfer application, and the script used to create that random data. The `results` directory stores the results of different network conditions. `file_transfer.py` contains the file transfer app.

# Group Members
1. Rohit Dwivedula (2017A7PS0029H)
2. Vamsi Nallappareddy (2017A7PS0018H)
3. Varad Kshirsagar (2017A7PS0141H)
4. Pranav Sista (2017A7PS1225H)
5. Shantanu Gupta (2017A7PS0137H)