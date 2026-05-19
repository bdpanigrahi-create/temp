FROM python:3.9-slim

WORKDIR /app

COPY billing_processor/requirements.txt /app/billing_processor/
RUN pip install -r /app/billing_processor/requirements.txt

COPY billing_processor/ /app/billing_processor/

EXPOSE 8080

CMD ["python", "billing_processor/app.py"]
