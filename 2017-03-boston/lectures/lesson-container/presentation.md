name: inverse
layout: true
class: center, middle, inverse
---
# Using reproducible container based environments
---
layout: false
### <span style="color:purple">Why do we need containers?</span>

### Science Reproducibility
--

  - Each project in a lab depends on complex software environments
    - operating system
    - drivers
    - software dependencies: Python/MATLAB/R + libraries
&nbsp;

--

  - We try to avoid
    - the computer I used was shut down a year ago, can’t rerun the results from my publication...
    - the analysis were run by my student, have no idea where and how...
    - etc.
---
### <span style="color:purple"> Why do we need containers?</span>
--

### Collaboration with your colleagues
--

- Sharing your code or using a repository might not be enough
--

- We try to avoid
  - well, I forgot to mention that you have to use Clang, gcc never worked for me...
  - don’t see any reason why it shouldn’t work on Windows...(I actually have no idea about Windows, but won’t say it...)
  - it works on my computer...
  - etc.
---
###<span style="color:purple">Why do we need containers?</span>

### Freedom to experiment!

--
- Universal Install Script from xkcd: *The failures usually don’t hurt anything...*
 And usually all your old programs work...

<img src="img/universal_install_script_2x.png" width="35%" />
--

- We try to avoid
  - I just want to Undo the last five hours of my life...
---
### <span style="color:purple">Virtual Machines and Container Technologies</span>

- Main idea -- isolate the computing environment
    - Allow regenerating computing environments
    - Allow sharing your computing environments

--

- Two main types:
  - Virtual Machines:
    - Virtualbox
    - VMware
    - AWS, Google Compute, ...
  - Containers:
    - Docker
    - Singularity

--

- The details differ (and matter depending on application)

---
### <span style="color:purple">Virtual Machines vs Containers</span>

<img src="img/Containers-vs-Virtual-Machines.jpg" width="80%" />

--

 **Virtual Machines**
  - emulate whole computer system (software+hardware)
  - run on top of a physical machine using a *hypervisor*
  - *hypervisor* shares and manages hardware of the host and executes the guest operating system
  - guest machines are completely isolated and have dedicated resources
---
### <span style="color:purple">Virtual Machines vs Containers</span>

  <img src="img/Containers-vs-Virtual-Machines.jpg" width="80%" />



   **Containers**
  - share the host system’s kernel with other containers
  - each container gets its own isolated user space
  - only bins and libs are created from scratch
  - **containers are very lightweight and fast to start up**

---
###<span style="color:purple">Docker</span>
- leading software container platform
- an open-source project
- **it runs now on Mac OS X and Windows (you don't have to run VM!)**

--

#### Testing your Docker installation:
  ```bash
  $ docker run hello-world
  ```
---
### <span style="color:purple">Docker: Using existing images</span>

- [Docker Hub](https://hub.docker.com/) -- repositories to share Docker images

- managing images:
  ```bash
  $ docker pull ubuntu
  $ docker images
  # remove images
  $ docker rmi <image_id>
  ```

- running containers
  ```bash
  $ docker run ubuntu
  $ docker run ubuntu echo ``hello from your container''
  ```
- `-it` option: running interactively
  ```bash
  $ docker run -it ubuntu bash
  ```
---
### <span style="color:purple">Docker: Using existing images</span>

- managing containers
  ```bash
  # list currently running containers
  $ docker ps
  # list created containers
  $ docker ps -a
  # remove containers
  $ docker rm <container_id>
  # remove all stops containers
  $ docker rm $(docker ps -a -q)
  ```
- `--rm` option: automatically removing the container when it exits
  ```bash
  $ docker run -it --rm ubuntu
  ```
- adding a data volume to a container (you can use multiple times to mount multiple data volumes)
  ```bash
  $ docker run -it --rm -v LocalDirectory:/src ubuntu
  # read only mode
  $ docker run -it --rm -v LocalDirectory:/src:ro ubuntu
  # you can mount multiple data volumes
  # the directory `temp` doesn't have to exist and will be created
  $ docker run -it --rm -v LocalDirectory:/src -v TempLocalDirectory:/temp ubuntu
  ```
---
### <span style="color:purple">Docker: Installing software with Dockerfile</span>

- Create a new directory

  ```bash
  $ mkdir mydockerbuild
  $ cd mydockerbuild
  ```

- Dockerfile content:

  ```bash
  FROM ubuntu:latest
  RUN apt-get update -y && apt-get install git emacs
  ```

- Building a new container:

  ```bash
  $ docker build -t my_new_container .
  ```

- Running your new container:

  ```bash
  $ docker run -it --rm my_new_container
  ```

- Within container you can try:
  ```bash
  $ git
  $ emacs
  ```
---
### <span style="color:purple">Docker: Installing software with Dockerfile</span>

- More about the Dockerfile syntax you can find [here](https://docs.docker.com/engine/reference/builder/#from)

- Example of Dockerfile to run Nipyp wokflow from [Docker Hub](https://hub.docker.com/r/miykael/nipype_level0/~/dockerfile/)
---
### <span style="color:purple">Docker and Nipype</span>

- Using Nipype official Docker image

  ```bash
  $ docker images
  # only if you haven't done it already
  $ docker pull miykael/nipype_level3
  $ docker run -it --rm miykael/nipype_level3 bash
  ```

- Within the nipype container

  ```bash
  python
  ```

- Within Python interpreter:

  ```python
  import nipype
  nipype.test()
  ```
---

### <span style="color:purple">Docker: running jupyter</span>

- Using Jupyter notebook with Docker container
`-p` option: publishing ports
  ```bash
  # you can use various host port number
  $ docker run -it --rm -p 9999:8888 miykael/nipype_level3
  ```
--

- Running local notebooks
TODO: wait for notebooks that will be used during workshop

---
### <span style="color:purple">Docker and Singularity</span>

- Docker:
  - docker can escalate privileges, so you can be effectively treated as a root on the host system
  - this is usually  not supported by HPC centers!

--

- Singularity:
  - a container solution created for scientific and application driven workloads
  - supports existing and traditional HPC resources
  - a user inside a Singularity container is the same user as outside the container
  - but you can use Vagrant to create a container (you have root privileges on your VM!)
  - can run (and modify!) existing Docker containers
  - running VM is required on OSX
  - [Satra's presentation](http://satra.cogitatum.org/om-images/)
  - [other tutorials](http://singularity.lbl.gov/tutorials)

---
### <span style="color:purple">Virtual Python environments and Conda</span>
- Virtual environments
  - keep the dependencies required by different projects in separate places
  - allows to work with specific versions of libraries or Python itself without affecting other Python projects

- Conda:
  - a package manager and an environment manager

---
### <span style="color:purple">Virtual Python environments and Conda</span>

- Using Conda for Python environments
  - if you don't have `conda` you can use `continuumio/miniconda` container
  - creating a new Python environment
  ```bash
  # updating conda
  $ conda update conda
  # listing available Python version
  $ conda search "^python$"
  # creating a Python 3.6 environment
  $ $ conda create -n python3.6_test python=3.6
  # this will also install all the associated anaconda packaged libraries
  $ conda create -n python3.6_anaconda python=3.6 anaconda
  ```
  - activating and deactivating the environment
  ```bash
  $ source activate python3.6_test
  $ source deactivate python3.6_test
  ```

  - installing additional packages
  ```bash
  $ conda install -n python3.6_test numpy
  ```

---
name: inverse
layout: true
class: center, middle, inverse
---
# Questions?
