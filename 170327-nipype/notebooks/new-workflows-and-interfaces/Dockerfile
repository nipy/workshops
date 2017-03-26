FROM miykael/nipype_course
MAINTAINER The nipype developers https://github.com/nipy/nipype

USER root
RUN apt-get update && \
    apt-get install -y octave && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    ln -s /usr/bin/octave /usr/bin/matlab
USER $NB_USER
