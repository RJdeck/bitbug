FROM python:3.10
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob
# Add crontab file to the cron.d directory
RUN crontab /etc/cron.d/cronjob

# Run the command on container startup
CMD ["cron", "-f", "-L", "15"]
