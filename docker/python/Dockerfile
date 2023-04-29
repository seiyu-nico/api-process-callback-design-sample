FROM python:3.9.16-bullseye

ARG USERNAME=dev
ARG GROUPNAME=dev
ARG UID=1000
ARG GID=1000
ENV TZ Asia/Tokyo

# ユーザー追加
RUN groupadd -g $GID $GROUPNAME && \
  useradd -m -s /bin/bash -u $UID -g $GID $USERNAME

# ユーザーのbinaryディレクトリをパスに追加
ENV PATH /home/$USERNAME/.local/bin:$PATH

RUN python -m pip install --upgrade --user pip && \
  python -m pip install --upgrade --user wheel && \
  python -m pip install --upgrade --user setuptools

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# ユーザー切り替え
USER $USERNAME
WORKDIR /src

ENTRYPOINT [ "/entrypoint.sh" ]
