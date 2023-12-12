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

## Guidelines for a Hands-On

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

### Step 4: **Install All Required Package for Flask Application**
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

**- Unit** — This section is for description about the project and some dependencies 

**- Service** — To specify user/group we want to run this service after. Also some information about the executables and the commands. 

**- Install** — tells systemd at which moment during boot process this service should start. 

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

Check if the app is running with


<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/gunicorn.png" >

### Step 8: **Configure Nginx as a Reverse Proxy**
```python
sudo apt install nginx
```
Start the Nginx service and go to the Public IP address of your EC2 on the browser to see the default nginx landing page.
```python
sudo systemctl start nginx
sudo systemctl enable nginx
```
**Next, create a new Nginx configuration file:**
```python
cd /etc/nginx/sites-enabled/
sudo nano jira
```
**Copy past following line:**
```python
server {
    listen 80;
    server_name 35.91.190.143;                  // public ip address of ec2 instance

    location / {
        proxy_pass http://127.0.0.1:8000;       // gunicorn local-address
    }
}
```
**Checking status of ngninx:**
```python
sudo service nginx restart
sudo systemctl status nginx
```
<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/nginx.png" >

### Step 9: **Configure github webhook**
**GitHub Webhooks: A Brief Overview**

GitHub webhooks provide a way for GitHub repositories to notify external services when certain events occur. These events can range from code pushes and pull requests to issues being opened or closed. Webhooks facilitate automated workflows and integrations by triggering actions in external systems in response to events within a GitHub repository.

**Key Components:**

 **Payloads:**
   - Webhooks send data payloads in JSON format to a specified URL when an event occurs.
   - The payload contains information about the event, such as the repository, the type of event, and relevant data associated with the event.

 **Events:**
   - GitHub supports a variety of events that can trigger webhooks, including `push` (code push), `pull_request` (pull request activity), `issues` (issue changes), and more.
   - Users can customize which events should trigger their webhook.

 **URL Endpoint:**
   - Users define a URL endpoint where GitHub sends the webhook payload.
   - This endpoint is typically the URL of an external service or an API endpoint in a custom application.

 **Security:**
   - GitHub allows users to set up a secret token for added security. This secret is used to create a hash of the payload, which is sent along with the payload to the receiving server. The receiving server can then verify the authenticity of the payload.

**Use Cases:**

 **Continuous Integration/Deployment (CI/CD):**
   - Webhooks can trigger CI/CD pipelines, automatically building and deploying code changes upon pushes to the repository.

 **Automated Testing:**
   - Hooks can initiate automated testing processes whenever new code is pushed, ensuring code quality and preventing regressions.

 **Issue Tracking:**
   - Webhooks can update external issue tracking systems whenever issues are opened, closed, or modified on GitHub.

 **Notifications:**
   - Integration with messaging services (Slack, Discord, etc.) to notify teams about important events in real-time.

**Setting Up GitHub Webhooks:**

  **Repository Settings:**
   - In the GitHub repository, navigate to "Settings" > "Webhooks."
   - Click "Add webhook" and provide the payload URL, set the events to trigger the webhook, and configure other settings.

  **Payload URL:**
   - Enter the URL where GitHub should send the payload (e.g., an endpoint in your application or a third-party service).

  **Secret (Optional):**
   - If security is a concern, users can set up a secret key that GitHub uses to sign the payload. The receiving server can then verify the payload's authenticity.

  **Testing the Webhook:**
   - GitHub provides a "Ping" event to test the webhook. After setup, it's recommended to perform a ping to ensure the webhook is configured correctly.
   <img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/webhook.png" >
   <img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/issue.png" >


GitHub webhooks are a powerful tool for automating and extending GitHub's functionality, allowing developers to integrate their workflows seamlessly with other tools and services.

**In this project, I am implementing to track issue comments use-case.**

### Step 10: **Result of Running Flask Application**

<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/project2.png" >

**Request and Response of Issue comment**

- /jira this is last test
<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/request_51.png" >
<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/response_51.png" >

- /abc this is another testing ticket
<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/request_abc.png" >
<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/response_abc.png" >

- /JIRA this is latest changes 
<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/request_52.png" >
<img src="https://github.com/CloudSantosh/jira_ticket_nginx_gunicorn_flask_application/blob/main/images/response_52.png" >
