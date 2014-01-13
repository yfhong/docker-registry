FROM netease/wheezy:base

RUN apt-get update
RUN apt-get install -y git-core python-pip build-essential python-dev libevent-dev python-openssl liblzma-dev
ADD . /srv/docker-registry
ADD ./config/boto.cfg /etc/boto.cfg

RUN cd /srv/docker-registry && pip install -r requirements.txt
RUN cp --no-clobber /srv/docker-registry/config/config_netease.yml /srv/docker-registry/config/config.yml

EXPOSE 5000

CMD cd /srv/docker-registry && ./setup-configs.sh && ./run.sh
