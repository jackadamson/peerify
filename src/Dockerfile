FROM python:3.7-stretch
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./peerify.py ./

CMD python peerify.py
