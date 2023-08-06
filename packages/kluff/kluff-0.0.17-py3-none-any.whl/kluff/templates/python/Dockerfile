FROM openfaas/of-watchdog:0.8.0 as watchdog
FROM python:3.10-slim

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
USER root
RUN chmod +x /usr/bin/fwatchdog

# Add non root user
RUN addgroup --system app && adduser app --system --ingroup app
RUN chown app /home/app

USER app
ENV PATH=$PATH:/home/app/.local/bin

WORKDIR /home/app/
USER app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . .

ENV fprocess="flask run"

ENV upstream_url="http://127.0.0.1:5000"
ENV mode="http"
ENV cgi_headers="true"

CMD ["fwatchdog"]
