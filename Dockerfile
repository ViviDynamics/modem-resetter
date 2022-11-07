FROM python:3.10.8-bullseye

RUN apt-get update -qq && apt-get upgrade -y
WORKDIR /opt/modem-resetter
COPY ./ /opt/modem-resetter

SHELL ["/bin/bash", "--login", "-c"]
RUN echo "Install project dependencies" && \
    cd /opt/modem-resetter && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

RUN chmod +x /opt/modem-resetter/bin/entrypoint
COPY bin/entrypoint /usr/bin/
RUN chmod +x /usr/bin/entrypoint
ENTRYPOINT ["entrypoint"]

CMD ['python3', 'main.py']
