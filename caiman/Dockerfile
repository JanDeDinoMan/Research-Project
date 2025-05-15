## Usage: `docker build -t janwillem/caiman:1.0 ./caiman`
#
#FROM continuumio/anaconda3:2024.10-1
#
#RUN conda config --set always_yes yes
#RUN conda update --yes conda
#RUN apt-get update && apt-get install -y gcc g++ libgl1
#COPY environment.yml environment.yml
#RUN conda env create -f environment.yml --verbose
#RUN /bin/bash -c "source activate caiman && caimanmanager install"
#
#ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--port=3000", "--allow-root", "--no-browser"]

FROM continuumio/miniconda3

# Set working directory
WORKDIR /root/caiman

# Copy the environment file
COPY environment.yml .

# Install Mamba and create the environment
RUN conda update -n base -c defaults conda && \
    conda install -n base -c conda-forge mamba && \
    mamba env create -f environment.yml&& \
    conda clean -afy

# Activate the environment by default in shell
SHELL ["conda", "run", "-n", "caiman-env", "/bin/bash", "-c"]

RUN caimanmanager install

# Ensure environment is on PATH
ENV PATH /opt/conda/envs/caiman-env/bin:$PATH

ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--port=3000", "--allow-root", "--no-browser"]
