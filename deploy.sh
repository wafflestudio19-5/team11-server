source ~/.bash_profile
cd ~/team11-server
source venv/bin/activate
export TEAM11_SERVER_ENV=1

if [ "$1" ] && [ "$1" = '--new' ] ; then
    #git pull origin master
    cat requirements.txt | xargs -n 1 pip3 install
fi

### django migration ###
cd everytime
if [ "$1" ] && [ "$1" = '--new' ] ; then
    python3 manage.py showmigrations
    python3 manage.py migrate
fi

### gunicorn ###
sudo fuser -k 8000/tcp
gunicorn --env TEAM11_SERVER_ENV=1 --bind 0.0.0.0:8000 everytime.wsgi:application -D
python3 manage.py check --deploy

### nginx ###
if [ -z "$1" ] && [ "$1" = '--new' ] ; then
    sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
    sudo cp ~/team11-server/conf/nginx.conf /etc/nginx/nginx.conf
fi
sudo nginx -t
sudo systemctl daemon-reload 
sudo service nginx restart
