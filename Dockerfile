FROM python:3

ADD controller.py /

ADD payload_validation.py /

COPY ./openapi.yaml /

RUN pip3 install tornado

RUN pip3 install requests

RUN pip3 install pyyaml

RUN pip3 install jsonref

RUN pip3 install asyncio

RUN pip3 install jsonschema

RUN pip3 install uuid

EXPOSE 8881

CMD ["python", "./controller.py"]

