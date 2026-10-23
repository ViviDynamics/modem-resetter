FROM python:3.10.8-bullseye

RUN apt-get update -qq && apt-get upgrade -y
WORKDIR /opt/modem-resetter
COPY ./ /opt/modem-resetter

SHELL ["/bin/bash", "--login", "-c"]
RUN echo "Install project dependencies" && \
    cd /opt/modem-resetter && \
    python -m pip install --no-cache-dir --no-deps \
      "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70" \
      "certifi @ https://files.pythonhosted.org/packages/c4/51/29046e48f693c54e5b7412216d447a1d8362c9653148d98c02cdf65fa733/certifi-2026.10.19-py3-none-any.whl#sha256=42d35340cc5b9ba78e818ddbff0c5b1c2b779de448a340fd1b989f5fa8670e1b" && \
    pip install -r requirements.txt

RUN chmod +x /opt/modem-resetter/bin/entrypoint
COPY bin/entrypoint /usr/bin/
RUN chmod +x /usr/bin/entrypoint
ENTRYPOINT ["entrypoint"]

CMD exec python3 main.py
