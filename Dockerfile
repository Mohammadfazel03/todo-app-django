FROM python:3.11-slim

ARG UID=0
ARG GID=0

RUN groupadd -g $GID -o django
RUN useradd -m -u $UID -g $GID -o -s /bin/bash django

ENV PATH /home/django/.local/bin:$PATH

WORKDIR /home/django
RUN chown -R $UID:$GID /home/django

USER django:django

COPY --chown=django requirements.txt .

RUN pip3 --timeout 1000 install --no-cache-dir  -r requirements.txt

COPY --chown=django . .

RUN chmod +x ./entry.sh

ENTRYPOINT ["./entry.sh"]
