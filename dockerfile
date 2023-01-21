# FROM mongo:4.4
FROM ubuntu
RUN apt-get update &&\
    apt-get install -y wget
# RUN mkdir /usr/app
# COPY miniconda.sh /usr/app
# RUN bash /usr/app/miniconda.sh -b -p /opt/conda

# Install miniconda
ENV CONDA_DIR /opt/conda
# RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
#      /bin/bash ~/miniconda.sh -b -p /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py38_4.11.0-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH
RUN cd $CONDA_DIR/bin && conda init 
# RUN pip install pymc3
RUN pip install notebook
# RUN pip install scikit-learn

# VOLUME mongo_data/ /data/db/

RUN  mkdir /home/app/
# RUN  mkdir /data/db
RUN  cd /home/app/
WORKDIR /home/app/

COPY --chown=developer:developer ./app/ /home/app
# COPY --chown=developer:developer ./gestao_dados/ /home/ethowatcher/gestao_dados
# COPY --chown=developer:developer ./running_jupyter_mongo.sh /home/ethowatcher/running_jupyter_mongo.sh

RUN pip install -r /home/app/requirements.txt
# RUN pip install -e /home/ethowatcher/gestao_dados/gestao-dados/
# RUN pip install -r /home/ethowatcher/gestao_dados/ethowatcher-server/requirements.txt


# installing node
# RUN apt-get install -y nodejs

# exposing jupyter
EXPOSE 8888
# exposing db port
EXPOSE 27017
# exposing interface port
EXPOSE  5000
# CMD [ "sh", "/home/ethowatcher/running_jupyter_mongo.sh" ]

CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--port", "8888", "--allow-root" ]

# docker run -p 8888:8888 -p 27017:27017 -p 5000:5000 -v C:\doutorado\software\EthoWatcherOS-docker\mongo_data\:/data/db "teste"
