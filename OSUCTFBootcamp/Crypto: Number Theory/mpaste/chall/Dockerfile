FROM tiangolo/uwsgi-nginx-flask:python3.8
WORKDIR /app
ENV STATIC_PATH /app/app/static
COPY ./app ./
RUN pip install --no-cache-dir -r requirements.txt

COPY gen_env.py ./
RUN python gen_env.py
RUN rm gen_env.py

RUN python -m flask init_db
