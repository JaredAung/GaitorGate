# Credentials Folder

## The purpose of this folder is to store all credentials needed to log into your server and databases. This is important for many reasons. But the two most important reasons is
    1. Grading , servers and databases will be logged into to check code and functionality of application. Not changes will be unless directed and coordinated with the team.
    2. Help. If a class TA or class CTO needs to help a team with an issue, this folder will help facilitate this giving the TA or CTO all needed info AND instructions for logging into your team's server. 


# Below is a list of items required. Missing items will causes points to be deducted from multiple milestone submissions.

1. Server URL or IP: http://18.222.76.244/
2. SSH username: ubuntu
3. SSH password or key: team3key.pem (Located in the credentials folder.)
4. Database URL or IP and port used.
    <br><strong> NOTE THIS DOES NOT MEAN YOUR DATABASE NEEDS A PUBLIC FACING PORT.</strong> But knowing the IP and port number will help with SSH tunneling into the database. The default port is more than sufficient for this class.
    Databade IP : 127.0.0.1         Port : 3306
5. Database username: team3admin
6. Database password: 12345
7. Database name (basically the name that contains all your tables): team3db
8. Instructions on how to use the above information.
   
    Server Access: On local machine terminal, navigate to the file that contains the key and enter this command.

       ssh -i team3Key.pem ubuntu@18.222.76.244
    
    Database Access: 
    
    Method 1 (Database Access in MySQL CLI)
    1. On local machine, open terminal and enter the following command for ssh tunnelling.
       
           ssh -i "absolute path to team3Key.pem" -L 3306:127.0.0.1:3306 ubuntu@18.222.76.244

    2. Once connected to the server, open a new terminal and run:

           mysql -u team3admin -p -h 127.0.0.1 -P 3306

    3. To verify connection, enter the following, team3db should be one of the listed databases.

           SHOW DATABASES; 

    5. It can also be connected to MySQL Workbench using the IP, Port, user name and password (SSH tunneling is  required). 



    Method 2 (MySQL Workbench)
   
    1. In MySQL Workbench, go to Database > Manage Connections > New Connection.
    2. Under Connection Method, select "Standard TCP/IP over SSH".
    3. Fill in the details:
       
            SSH Hostname : 18.222.76.244
       
            SSH Username :ubuntu
       
            SSH Key File : /absolute/path/to/team3Key.pem
       
            MySQL Hostname : 127.0.0.1
       
            MySQL Port : 3306
       
            Username: team3admin
       
            Password: 12345
       
            Click Test Connection.

If accessing the root of mysql, 

Username: root

Password: MaThuZar2002$
# Most important things to Remember
## These values need to kept update to date throughout the semester. <br>
## <strong>Failure to do so will result it points be deducted from milestone submissions.</strong><br>
## You may store the most of the above in this README.md file. DO NOT Store the SSH key or any keys in this README.md file.
