FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HOST_URL=<host_url>
ENV API_KEY=<api_key>
ENV TEMPORARY_FOLDER=<temporary_folder>
ENV KEEP_TIME=<keep_time>
ENV RECURRENCE=<recurrence>

CMD [ "python", "TempArr.py" ]