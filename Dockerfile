FROM python:3.8

WORKDIR /app/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY clock_in_clock_out/ ./clock_in_clock_out/
COPY app.py .

CMD [ "python3", "app.py" ]