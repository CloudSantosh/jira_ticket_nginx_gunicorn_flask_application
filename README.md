# Deploying a Flask Application on EC2


<br>

<img src="https://github.com/CloudSantosh/jira_ticket_github_webhook_python_API/blob/main/images/app.png" >

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

