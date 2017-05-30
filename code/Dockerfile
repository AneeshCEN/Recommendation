FROM python:2.7
ENV PYTHONUNBUFFERED 1
#RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code
EXPOSE 3017
CMD ["uwsgi" , "--check-static", "rest_framework" ,"--wsgi-file", "Recommendation/wsgi.py", "--master", "--http", "0.0.0.0:3017"]

