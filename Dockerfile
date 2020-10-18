FROM python:3.8

WORKDIR /app/

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY clock_in_clock_out/ /app/clock_in_clock_out/
COPY app.py /app/app.py

COPY sample_data.xml /app/sample_data.xml

ENTRYPOINT [ "python3", "app.py" ]