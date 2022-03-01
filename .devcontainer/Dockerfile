FROM jupyter/datascience-notebook

WORKDIR /workdir

COPY requirements.txt /workdir/

RUN pip install --upgrade pip
RUN pip install -r /workdir/requirements.txt
