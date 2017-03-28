name: inverse
layout: true
class: center, middle, inverse
---
# Capturing details of analysis
### satra@mit.edu
#### License: CC0
---
layout: false
.left-column[
  ## Outline
]
.right-column[

### Learning objectives

### Requirements

### Introduction

### Exercises

### Review questions
]
---
.left-column[
## Learning objectives
]
.right-column[
- Why to capture details of analysis

- How to capture details of analysis

- How to use the captured information
]
---
.left-column[
## Learning objectives
## Requirements
]
.right-column[

- Unix shell basics

- Docker + docker image: .red[???]

  Provides:

  - strace, ltrace, ptrace
  - Nipype
  - Reprozip

]
---
.left-column[
## Introduction
]
.right-column[
- Why collect analysis information ?

  - To document/disseminate what was done
  - To repeat an analysis
  - To compare across analyses
  - To understand sources of variance
]
---
.left-column[
## Introduction
]
.right-column[
- Why collect analysis information ?

  - To document/disseminate what was done
  - To repeat an analysis
  - To compare across analyses
  - To understand sources of variance

- What types of information should you collect about your analysis?

  - Data
  - Parameters
  - Environment
     - Hardware
     - Operating system
     - Software/libraries
  - Code
  - Output
  - Requirements
]
---
.left-column[
## Introduction
## Tools
]
.right-column[

- **[`script`][1]**

  A terminal tool to record shell commands available on all Unix systems.

- **[`reprozip`](https://www.reprozip.org/)**

  A Python tool to capture details of a run.

- **[`strace`](https://blog.packagecloud.io/eng/2016/02/29/how-does-strace-work/)**

  A tool to capture system calls made by a script.

]
---
.left-column[
## Introduction
## Tools
]
.right-column[

- **[`script`][1]**

  A terminal tool to record shell commands available on all Unix systems.

- **[`reprozip`](https://www.reprozip.org/)**

  A Python tool to capture details of a run.

- **[`strace`](https://blog.packagecloud.io/eng/2016/02/29/how-does-strace-work/)**

  A tool to capture system calls made by a script.

#### Mapping requirements (L: Limited, F: Full, X: Unavailable)

| | script&nbsp;&nbsp;&nbsp; | .blue[reprozip]&nbsp;&nbsp;&nbsp; | strace |
|-|-|-|-|-|
| Data | L | F | L |
| Parameters | F | F | F |
| Hardware | X | L | X |
| OS | X | L | X |
| Software | X | F | F |
| Code | L | F | F |
| Output | L | F | L |
| Requirements&nbsp;&nbsp;&nbsp; | X | X | X |

]
[1]: https://en.wikipedia.org/wiki/Script_(Unix)
---
.left-column[
## Introduction
## Tools
## Quirks
]
.right-column[

- All tools require a Unix system and will not run directly on Windows

- Running on Mac OS requires giving docker some system privileges, by adding the
  following flag.

  ```
  --security-opt seccomp:unconfined
  ```

- `strace` is not always available by default. You may need to install it from
  the package repository.

  For debian/ubuntu: `sudo apt-get install strace`

  On Mac OS, strace is replaced by the system command `dtrace`. However, this
  requires administrator level privileges to run.

- Reprozip uses `ptrace` calls under the hood and will only run, at present (Mar
  2017) on systems that have the capability at user level (not MacOS).

- If you are calling remote services, or submitting jobs, each job would need to
  run its own trace.
]
---
.left-column[
## Introduction
## Tools
## Quirks
## Other tools
]
.right-column[

- ** [Sumatra](http://neuralensemble.org/sumatra/) **

- ** [Common Workflow Language](http://www.commonwl.org/) **

- ** [Nipype](http://nipype.readthedocs.io/en/latest/devel/provenance.html) **

- ** [Niceman](https://github.com/ReproNim/niceman) **

- ** [Asciinema](https://asciinema.org/) **
]
---
.left-column[
## Introduction
## Tools
## Quirks
## Other tools
## Examples
]
.right-column[

1. Using `script`

2. Using `reprozip`

.footnote[.red[\*] We will skip `strace` for this lesson.]
]
---
class: middle
## Let's get started

```bash
  docker run -it --rm -v /software/work:/home/jovyan/work --security-opt
    seccomp:unconfined --name repeat nipype/workshops:latest-nofsspm bash

  jovyan@73a1924ff93c:~/work$ mkdir reprozip
  jovyan@73a1924ff93c:~/work$ cd reprozip
```
---
## Using `script`
.left-column2[
Let us turn on script mode. All output will be in a file named `typescript`.
```bash
$ script
```

Now let us type some commands and then exit script mode with `Ctrl+D`
```bash
$ which script
$ man script
$ Ctrl+D
```

Now let us examine what the file typescript contains.
```bash
$ more typescript
```
]
.right-column2[
** Video tutorial (Opens in a new window) **

<a href="https://asciinema.org/a/108382" target="\_blank"><img src="https://asciinema.org/a/108382.png" width="100%"/></a>

]
---
## Using `reprozip`

If you don't have reprozip you can install it into a python environment.
```bash
$ pip install reprozip
```
--
As with many commands, you can type `reprozip` to get help
```bash
$ reprozip
...
commands:

    usage_report        Enables or disables anonymous usage reports
    trace               Runs the program and writes out database and
                        configuration file
    testrun             Runs the program and writes out the database contents
    reset               Resets the configuration file
    pack                Packs the experiment according to the current
                        configuration
    combine             Combine multiple traces into one (possibly as
                        subsequent runs)
```
---
## Using `reprozip`

For a first example we will use `reprozip` on running `bet` from the command line.
```bash
$ reprozip trace -d bet-trace bet
     ../data/ds000114/sub-01/anat/sub-01_T1w.nii.gz brain
```
--
This creates a `config.yml` file in the directory `bet-trace`
```bash
$ more bet-trace/config.yml
```
--
We can take look at each section of this file.
```bash
$ cat bet-trace/config.yml | grep "^[^# -].*:"
version: "0.8"
runs: --> This is a list of reprozip runs
inputs_outputs: --> These are the inputs and outputs of each run
packages: --> These are packages from which files were used
other_files: --> These are all files that were used during the process
```
---
## Take a closer look at each section: `runs`

`runs` is a list collecting information about each run save to a trace directory.

```yaml
runs:
- architecture: x86_64
  argv: [bet, ../data/ds000114/sub-01/anat/sub-01_T1w.nii.gz, brain]
  binary: /usr/lib/fsl/5.0/bet
  distribution: [debian, '8.7']
  environ: {
    FSLDIR: /usr/share/fsl/5.0,
    FSLMULTIFILEQUIT: 'TRUE',
    FSLOUTPUTTYPE: NIFTI_GZ,
    HOME: /home/jovyan,
    LD_LIBRARY_PATH: '/usr/lib/fsl/5.0:',
    PATH: '/opt/PALM:/opt/afni:/opt/c3d/bin:/opt/ants:/usr/lib/fsl/5.0:
        /opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:
            /usr/bin:/sbin:/bin',
  exitcode: 0
  gid: 100
  hostname: 25b88f158a09
  id: run0
  system: [Linux, 4.9.13-moby]
  uid: 1000
  workingdir: /home/jovyan/work/reprozip
```
---
## Take a closer look at each section: `inputs_outputs`

A description from `reprozip`
```text
# Input and output files

# Inputs are files that are only read by a run; reprounzip can replace these
# files on demand to run the experiment with custom data.
# Outputs are files that are generated by a run; reprounzip can extract these
# files from the experiment on demand, for the user to examine.
# The name field is the identifier the user will use to access these files.
```
--
The output from the run.
```yaml
inputs_outputs:
- name: arg
  path: /home/jovyan/work/data/ds000114/.git/annex/objects/QP/jm/
    MD5E-s8677710--d6820f6cb8fb965e864419c14f6a22d5.nii.gz/
    MD5E-s8677710--d6820f6cb8fb965e864419c14f6a22d5.nii.gz
  written_by_runs: []
  read_by_runs: [0]
- name: brain.nii.gz
  path: /home/jovyan/work/reprozip/brain.nii.gz
  written_by_runs: [0]
  read_by_runs: []
```
---
## Take a closer look at each section: `packages`

A description from `reprozip`
```text
# These files come from packages; we can thus choose not to include them, as it
# will simply be possible to install that package on the destination system
# They are included anyway by default
```
--
```yaml
packages:
  - name: "coreutils"
    version: "8.23-4"
    size: 14590976
    packfiles: true
    files:
      # Total files used: 58.66 KB
      # Installed package size: 13.92 MB
      - "/bin/rm" # 58.66 KB
  - name: "dash"
    version: "0.5.7-4+b1"
    size: 195584
    packfiles: true
    files:
      # Total files used: 122.46 KB
      # Installed package size: 191.00 KB
      - "/bin/dash" # 122.46 KB
      - "/bin/sh" # Link to /bin/dash
...
```
---
## Take a closer look at each section: `packages`

```yaml
...
- name: "fsl-5.0-core"
  version: "5.0.9-3~nd80+1"
  size: 40948736
  packfiles: true
  files:
    # Total files used: 2.60 MB
    # Installed package size: 39.05 MB
    - "/usr/lib/fsl/5.0/bet" # 13.41 KB
    - "/usr/lib/fsl/5.0/bet2" # 75.13 KB
    - "/usr/lib/fsl/5.0/imtest" # 4.29 KB
    - "/usr/lib/fsl/5.0/libfslio.so" # 50.61 KB
    - "/usr/lib/fsl/5.0/libfslvtkio.so" # 86.88 KB
    - "/usr/lib/fsl/5.0/libmeshclass.so" # 98.85 KB
    - "/usr/lib/fsl/5.0/libmiscmaths.so" # 569.38 KB
    - "/usr/lib/fsl/5.0/libnewimage.so" # 1.63 MB
    - "/usr/lib/fsl/5.0/libprob.so" # 31.93 KB
    - "/usr/lib/fsl/5.0/libutils.so" # 50.59 KB
    - "/usr/lib/fsl/5.0/remove_ext" # 4.06 KB
    - "/usr/share/fsl/5.0/bin" # Link to /usr/lib/fsl/5.0
...
```
---
## Take a closer look at each section: `other_files`

A description from `reprozip`
```text
# These files do not appear to come with an installed package -- you probably
# want them packed
```
Additional files needed for the run
```yaml
other_files:
  - "/etc/ld.so.cache" # 26.46 KB
  - "/home/jovyan/work/data/ds000114/.git/annex/objects/QP/jm/
     MD5E-s8677710--d6820f6cb8fb965e864419c14f6a22d5.nii.gz/
     MD5E-s8677710--d6820f6cb8fb965e864419c14f6a22d5.nii.gz" # 8.28 MB
  - "/home/jovyan/work/data/ds000114/sub-01/anat/sub-01_T1w.nii.gz"
     # Link to /home/jovyan/work/data/ds000114/.git/annex/objects/QP/jm/
       MD5E-s8677710--d6820f6cb8fb965e864419c14f6a22d5.nii.gz/
       MD5E-s8677710--d6820f6cb8fb965e864419c14f6a22d5.nii.gz
  - "/home/jovyan/work/reprozip" # Directory
  - "/lib64/ld-linux-x86-64.so.2" # Link to /lib/x86_64-linux-gnu/ld-2.19.so
  - "/usr/lib/fsl/5.0" # Directory
```
---
## Packing this analysis

First, we can pack this analysis into a reprozip pack file.
```bash
$ reprozip pack -d bet-trace better.rpz
$ ls -alh better.rpz
-rw-r--r-- 1 root root 17M Mar 22 18:06 better.rpz
```
This file now contains all the data and code to reproduce the analysis.

--

Let's quit docker, and get a container with no FSL, no Neurodebian.
```bash
$ docker pull continuumio/miniconda
$ docker run -it --rm -v /software/work/reprozip:/src continuumio/miniconda bash
```
---
## Replaying the analyis

Now we need the counterpart of `reprozip` a.k.a .red[`reprounzip`].

```bash
$ pip install reprounzip
$ reprounzip
...
subcommands:

    usage_report
                 Enables or disables anonymous usage reports
    chroot       Unpacks the files and run with chroot
    directory    Unpacks the files in a directory and runs with PATH and
                 LD_LIBRARY_PATH
    graph        Generates a provenance graph from the trace data
    info         Prints out some information about a pack
    installpkgs  Installs the required packages on this system
    showfiles    Prints out input and output file names
```
---
## Replaying this analysis

We will use the `chroot` form of replaying the analysis, allowing isolation.
```bash
$ reprounzip chroot -h
usage: reprounzip chroot [-h] [--version]

Unpacks the files and run with chroot

    setup/create    creates the directory (needs the pack filename)
    setup/mount     mounts --bind /dev and /proc inside the chroot
                    (do NOT rm -Rf the directory after that!)
    upload          replaces input files in the directory
                    (without arguments, lists input files)
    run             runs the experiment
    download        gets output files
                    (without arguments, lists output files)
    destroy/unmount unmounts /dev and /proc from the directory
    destroy/dir     removes the unpacked directory
```
--
So let's unpack the reprozip file into a directory called `better`.
```bash
$ reprounzip chroot setup --dont-bind-magic-dirs better.rpz better
```
---
## Replaying this analysis

Let's look at what the setup unpacked
```bash
$ ls better
config.yml  inputs.tar.gz  root
$ls better/root
bin  etc  home	lib  lib64  usr
$ ls better/root/home/jovyan/work/data/ds000114/sub-01/anat/sub-01_T1w.nii.gz
better/root/home/jovyan/work/data/ds000114/sub-01/anat/sub-01_T1w.nii.gz
$ ls better/root/home/jovyan/work/reprozip/
```

--
Now rerun the analysis
```bash
$ reprounzip chroot run better

*** Command finished, status: 0

$ ls better/root/home/jovyan/work/reprozip/
brain.nii.gz
```
---
## Review questions

1. What does `script` help you with?

2. What types of information does `reprozip` capture about an analysis?

3. What do you need to run `reprozip`?

4. On what platforms can you run `reprozip`?

5. What do you need to run `reprounzip`?

6. On what platforms can you run `reprozip`?

---
class: middle center

## Any questions?
