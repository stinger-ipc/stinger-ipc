FROM gitpod/workspace-python

USER gitpod
RUN sudo install-packages python3-pip
ADD --chown=gitpod https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py /tmp/get-poetry.py
RUN cat /tmp/get-poetry.py | python3 -

ENV PATH=$PATH:$HOME/.poetry/bin