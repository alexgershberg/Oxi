FROM python:3.8.14-alpine3.16
WORKDIR /code
ADD logger.py .
COPY oxi_json_typing oxi_json_typing
ENV FLASK_APP=logger.py
ENV FLASK_DEBUG=true
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "2515"]
