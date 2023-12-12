## Flask Application Delivery: A Comprehensive Guide to Nginx as Web Server and Gunicorn as WSGI Server in a Production Environment


<br>

<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/app.png" >

Nginx works as a web server and reverse proxy in conjunction with Gunicorn as a WSGI application server to serve a Flask application.

### 1. **Client Makes a Request:**
   - A user or client makes an HTTP request to your server by entering a URL in their browser or using a tool like `curl` or a webhook provider.

### 2. **Request Reaches Nginx:**
   - Nginx, configured as a web server, listens for incoming requests on port 80 (or another specified port).
   - The request reaches Nginx, which acts as the entry point to your server.

### 3. **Nginx Handles Static Files:**
   - If the request is for a static file (e.g., an image, CSS file, or JavaScript file), Nginx can serve it directly without involving the application server.
   - This improves performance and efficiency for static assets.

### 4. **Request for Dynamic Content:**
   - If the request is for dynamic content (e.g., a web page generated by a Flask application), Nginx forwards the request to the configured upstream server.

### 5. **Nginx as a Reverse Proxy:**
   - Nginx is configured as a reverse proxy to forward requests to the Gunicorn server, which is running your Flask application.
   - The configuration might include settings like `proxy_pass` to specify the backend server's address and port.

### 6. **Request Reaches Gunicorn:**
   - Gunicorn (Green Unicorn) is a WSGI application server that serves your Flask application.
   - It listens for requests from Nginx on a specified port (e.g., 8000).

### 7. **Gunicorn Handles the Request:**
   - Gunicorn receives the forwarded request and passes it to the Flask application for processing.

### 8. **Flask Application Processes the Request:**
   - Flask application processes the request, executes the appropriate route handler, and generates the dynamic content.

### 9. **Flask Application Sends Response to Gunicorn:**
   - The Flask application sends the generated response back to Gunicorn.

### 10. **Gunicorn Sends Response to Nginx:**
   - Gunicorn sends the response back to Nginx.

### 11. **Nginx Sends Response to the Client:**
   - Nginx receives the response from Gunicorn and forwards it to the client that made the initial request.

### 12. **Client Receives the Response:**
   - The client (e.g., web browser) receives the HTTP response and displays the requested content.

### 13. **Closing Connections:**
   - Nginx and Gunicorn manage and close the connections appropriately.

This setup is common for deploying Flask applications in production, offering a balance between performance, scalability, and ease of configuration.

## Guidelines for a Hands-On Approach

### Prerequisites
Before we begin, make sure you have the following:
- An AWS account with EC2 access.
- An EC2 instance set up with a proper security group allowing HTTP/HTTPS traffic (port 80/443).
- A Flask application that you want to deploy


### Step 1: **Connect to Your EC2 Instance**
Use SSH or EC2 Instance connect to connect to your EC2 instance. You can use the public IP or DNS of your instance and the private key you used when creating the instance.

### Step 2: **Prepare EC2 Environment**
- Install Required Packages

Update the package manager and install necessary packages like Python

```python
sudo apt update
sudo apt-get install python3-venv
 ```

### Step 3: **Set Up a Virtual Environment**
Creating a virtual environment ensures that your application dependencies won’t interfere with other Python projects on the same machine.

**create a new directory**

```python
mkdir jira
cd jira
 ``` 

**create a virtual environment inside jira**

```python
python3 -m venv venv
 ``` 
**activate the virtual environment**
```python
source venv/bin/activate
 ``` 

### Step 4: **Install All Required Package for Flask Application **
```python
sudo apt install python3-flask
pip3 install requests
sudo apt-get install python3-dotenv
 ``` 
### Step 5: **Create Flask API**
**create a new python file called app.py using nano editor.**
```python
 sudo nano app.py
  ``` 
**Now copy the code [[app.py]](https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/app.py) and save.**

**verify it by running the below command**
```python
 python3 app.py
  ``` 
Press CTRL + C to exit.

You will probably get a warning because its running on http://127.0.0.1:5000 [local host : portnumber]

Its asking use to run this application in WSGI server.


**create a new environment variable called .env using nano editor.**
```python
 sudo nano .env
  ```  
save the Jira api token and its email address. 
```python
JIRA_API_TOKEN = "xxxxxxxxxxxx" 
JIRA_EMAIL = "xxxxxx@gmail.com" 
  ```

Create a folder called templates where **[result.html](https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/templates/result.html)** file is created to receive response of flask application. 

### Step 6: **SetUp Gunicorn**
```python
sudo apt install gunicorn
or 
pip install gunicorn
  ```

### Step 7: **Test the Application Locally**
Before deploying, ensure that your application works locally with Gunicorn.
```python
gunicorn -b 0.0.0.0:8000 [replace with your app name]:app 

or gunicorn [replace with your app name]:app 
  ```
<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/gunicorn1.png" >

In my case my app name is **app** only so make sure to replace it with your app name.

Gunicorn is running (Ctrl + C to exit gunicorn)!

Use systemd to manage Gunicorn Systemd is a boot manager for Linux. We are using it to restart gunicorn if the EC2 restarts or reboots for some reason. We create a .service file in the /etc/systemd/system folder, and specify what would happen to gunicorn when the system reboots. We will be adding 3 parts to systemd Unit file — Unit, Service, Install

- Unit — This section is for description about the project and some dependencies 
- Service — To specify user/group we want to run this service after. Also some information about the executables and the commands. 
- Install — tells systemd at which moment during boot process this service should start. 

With that said, create an unit file in the /etc/systemd/system directory

```python
sudo nano /etc/systemd/system/jira.service
  ```

paste the below code

```python

[Unit]
Description=Gunicorn instance for  app
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/jira
ExecStart=/home/ubuntu/jira/venv/bin/gunicorn -b 127.0.0.1:8000 app:app
Restart=always
[Install]
WantedBy=multi-user.target

  ```
Now enable the service:

```python
sudo systemctl daemon-reload
sudo systemctl start jira
sudo systemctl enable jira
```

sudo apt update
sudo apt-get install python3-venv
clear 
    2  mkdir jira
    3  cd jira/
    4  mkdir templates
    5  cd templates/
    6  sudo nano index.html
    7  sudo nano result.html
    8  cd ..
    9  sudo nano app.py
   10  python3 -m venv venv
   11  sudo apt install python3.10-venv
   12  sudo apt update
   13  sudo apt-get install python3-venv
   14  python3 -m venv venv
   15  clear
   16  python3 -m venv venv /jira
   17  sudo python3 -m venv venv /jira
   18  sudo python3 -m venv venv
   19  source venv/bin/activate
   20  clear
   21  pip install flask
   22  flask
   23  pip3 install requests
   24  pip install requests
   25  sudo apt install python3-flask
   26  sudo pip3 install python-dotenv
   27  sudo apt-get  install python-dotenv
   28  sudo apt-get  install python3-dotenv
   29  history
   30  python3 app.py 
   31  sudo apt-get install python3-dotenv
   32  python3 app.py 
   33  sudo pip3 install python-dotenv
   34  sudo pip install python-dotenv
   35  python app.py 
   36  ls
   37  clear 
   38  gunicorn -b 0.0.0.0 app:app
   39  sudo apt install gunicorn
   40  gunicorn -b 0.0.0.0 app:app
   41  gunicorn -b 0.0.0.0:8000 app:app
   42  whereis gunicorn
   43  gunicorn -b 0.0.0.0:8000 app:app
   44  nginx
   45  sudo apt install nginx
   46  cd /etc/nginx/sites-enabled/
   47  sudo nano jira
   48  sudo service nginx restart
   49  sudo systemctl status nginx
   50  cd ..
   51  ls
   52  cd usr/
   53  ls
   54  cd ..
   55  ls
   56  cd jira/
   57  ls
   58  cd include/
   59  cd ..
   60  cd bin/
   61  ls
   62  cd ..
   63  cd  ..
   64  cd home/
   65  ls
   66  cd ubuntu/
   67  ls
   68  cd jira/
   69  ls
   70  gunicorn app:app
   71  sudo nano app.py 
   72  sudo nano .env
   73  sudo service nginx restart
   74  gunicorn app:app
   75  sudo nano app.py 
   76  gunicorn app:app
   77  sudo nano /etc/nginx/sites-enabled/
   78  sudo nano /etc/nginx/sites-enabled/jr
   79  sudo nano /etc/nginx/sites-enabled/jira 
   80  sudo nano /etc/systemd/system/jira.service
   81  sudo systemctl daemon-reload
   82  sudo systemctl start jira
   83  sudo systemctl enable jira
   84  sudo systemctl status jira
   85  whereis gunicorn
   86  sudo nano /etc/systemd/system/jira.service
   87  sudo systemctl daemon-reload
   88  sudo systemctl start jira
   89  sudo systemctl enable jira
   90  sudo systemctl status jira
   91  pip3 install gunicorn2
   92  pip3 install gunicorn
   93  whereis gunicorn
   94  sudo systemctl daemon-reload
   95  sudo systemctl start jira
   96  sudo systemctl enable jira
   97  sudo systemctl status jira
   98  ls
   99  sudo nano app.py 
  100  cd templates/
  101  ls
  102  nano result.html 

  configuration of /etc/nginx/sites-enabled/jira
server {
    listen 80;
    server_name 35.91.190.143; //ec2  ipaddress

    location / {
        proxy_pass http://127.0.0.1:8000; //gunicorn_localaddress

    }

}

sudo service nginx restart

Configuration of gunicorn 
sudo nano /etc/systemd/system/jira.service


