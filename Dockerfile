FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

ENV MASTODON_URL=""
ENV ACCESS_TOKEN=""
ENV TARGET_USER_ID=""
ENV CHECK_INTERVAL=300

CMD ["python", "bot.py"]

