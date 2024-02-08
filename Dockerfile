FROM python:latest

WORKDIR /usr/src/app

COPY . .

RUN pip install . && pip install -r requirements-dev.txt
RUN useradd --uid 1000 -m user
USER user
WORKDIR /home/user
ENTRYPOINT ["/usr/local/bin/fhs-xmltv-tools"]
