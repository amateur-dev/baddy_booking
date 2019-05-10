FROM python:latest
WORKDIR /home
COPY . .
RUN alias pip=pip3
RUN alias python=python3
RUN pip3 install -r requirements.txt
CMD tail -f /dev/null
# CMD python main.py