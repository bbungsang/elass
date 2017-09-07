FROM            bbungsang/elass
MAINTAINER      bbungsang@gmail.com

# 현재 경로의 모든 파일을 컨테이너의 /srv/elass 폴더에 복사
COPY            . /srv/elass

# cd /srv/elass 과 같은 효과
WORKDIR         /srv/elass

# requirements 설치
RUN             /root/.pyenv/versions/elass/bin/pip install -r .requirements/deploy.txt

# supervisor 파일 복사
COPY            .config/supervisor/uwsgi.conf /etc/supervisor/conf.d/
COPY            .config/supervisor/nginx.conf /etc/supervisor/conf.d/

# nginx 파일 복사
COPY            .config/nginx/nginx.conf /etc/nginx/nginx.conf
COPY            .config/nginx/nginx-app.conf /etc/nginx/sites-available/nginx-app.conf
# 기존 80 포트 요청을 받는 default 제거
RUN             rm -rf /etc/nginx/sites-enabled/default
# symbolic link 생성
RUN             ln -sf /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/nginx-app.ini

# collectstatic 실행
RUN             /root/.pyenv/versions/elass/bin/python /srv/elass/django_app/manage.py collectstatic --settings=config.settings.deploy --noinput

CMD             supervisord -n

# 컨테이너 내부 어느 포트와 연결시킬 것인지에 대한 커맨드 : nginx 가 80 포트 요청을 받기 때문에 80 으로 지정
EXPOSE          80