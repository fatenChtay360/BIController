FROM python:3

ADD controller.py /

COPY ./BI.json /

RUN pip3 install tornado

RUN pip3 install requests

RUN pip3 install pyyaml

RUN pip3 install jsonref

RUN pip3 install asyncio

RUN pip3 install jsonschema

EXPOSE 8881

CMD ["python", "./controller.py"]
