FROM python:3.8-alpine
WORKDIR /code
ADD app.py .
COPY oxi_json_typing oxi_json_typing
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]