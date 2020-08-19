FROM python:3

ADD controller.py /

RUN pip3 install tornado

RUN pip3 install requests


RUN pip3 install asyncio


EXPOSE 8881

CMD ["python", "./controller.py"]

