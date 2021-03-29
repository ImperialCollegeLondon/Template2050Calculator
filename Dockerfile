FROM anvil-app-server

USER root

COPY requirements.txt /apps

RUN pip install --no-cache-dir -r /apps/requirements.txt

EXPOSE 3030
