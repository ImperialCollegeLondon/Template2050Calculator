FROM ghcr.io/imperialcollegelondon/anvil-app-server:latest
ENTRYPOINT []

USER root

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# Add the below just in case the preceding pip install changes the version of
# anvil-app-server
RUN anvil-app-server || true
EXPOSE 3030

USER anvil
COPY --chown=anvil:anvil . /apps/Template2050Calculator/
