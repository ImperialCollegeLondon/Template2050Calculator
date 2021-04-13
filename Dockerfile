FROM anvil-app-server

USER root

COPY * /apps/Template2050Calculator/

RUN pip install --no-cache-dir -r /apps/Template2050Calculator/requirements.txt

EXPOSE 3030

USER anvil

CMD ["--app", "/apps/Template2050Calculator"]
