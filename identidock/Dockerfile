FROM python:3.7-slim

# Создаём пользователя uwsgi
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

# Устанавливаем компилятор и зависимости для сборки uWSGI
RUN apt-get update && apt-get install -y \
        build-essential \
        python3-dev \
        libpcre3-dev \
        libpcre3 \
    && pip install --upgrade pip \
    && pip install Flask==0.10.1 \
                   Jinja2<3.0 \
                   Werkzeug<2.0 \
                   itsdangerous<2.0 \
                   MarkupSafe<2.0 \
                   uWSGI==2.0.19.1 \
                   requests==2.5.1 \
                   redis==2.10.3 \
    && apt-get remove -y build-essential python3-dev libpcre3-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*



WORKDIR /app
COPY app /app
COPY cmd.sh /

EXPOSE 9090 9191
USER uwsgi

CMD ["/cmd.sh"]
