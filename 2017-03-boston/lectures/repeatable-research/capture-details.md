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

### Tools

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

2. An example of `strace` output

3. Using `reprozip`
]
---
class: middle
## Let's get started

```bash
  docker run -it --rm --security-opt seccomp:unconfined -v bids-data:/data
    -v $PWD:/src/workdir test36:trace bash

  root@b6d7839a5760:/src/workdir#
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
$ cat typescript | grep '^# [^#]'
```
]
.right-column2[
** Video tutorial (Opens in a new window) **

<a href="https://asciinema.org/a/108382" target="\_blank"><img src="https://asciinema.org/a/108382.png" width="100%"/></a>

]
---
## Using `reprozip`

As with many commands, you can type `reprozip` to get help
```bash
$ reprozip
```
--
For a first example we will use `reprozip` on running `bet` from the command line.
```bash
$ reprozip trace -d bet-trace bet sub-01_T1w.nii.gz brain
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
  argv: [bet, sub-01_T1w.nii.gz, brain]
  binary: /usr/lib/fsl/5.0/bet
  distribution: [debian, stretch/sid]
  environ: {
    ACCEPT_INTEL_PYTHON_EULA: 'yes',
    HOME: /root, HOSTNAME: 72bfac9cef1d, LANG: C.UTF-8, LC_ALL: C.UTF-8,
    LD_LIBRARY_PATH: '/usr/lib/fsl/5.0:',
    OMP_NUM_THREADS: '1', OS: Linux,
    PATH: '/usr/local/miniconda/bin:/usr/lib/ruby/gems/2.3/bin:/bin::
        /usr/lib/fsl/5.0:/usr/lib/afni/bin:/opt/freesurfer/bin:/opt/
        freesurfer/fsfast/bin:/opt/freesurfer/tktools:/opt/freesurfer/
        mni/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'}
  exitcode: 0
  gid: 0
  hostname: 72bfac9cef1d
  id: run0
  system: [Linux, 4.9.12-moby]
  uid: 0
  workingdir: /src/workdir
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
  path: /src/workdir/sub-01_T1w.nii.gz
  written_by_runs: []
  read_by_runs: [0] ---> This is an input
- name: brain.nii.gz
  path: /src/workdir/brain.nii.gz
  written_by_runs: [0]  ----> This is an output
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
      version: "8.25-2ubuntu2"
      size: 6414336
      packfiles: true
      files:
        # Total files used: 58.86 KB
        # Installed package size: 6.12 MB
        - "/bin/rm" # 58.86 KB
    - name: "dash"
      version: "0.5.8-2.1ubuntu2"
      size: 247808
      packfiles: true
      files:
        # Total files used: 150.46 KB
        # Installed package size: 242.00 KB
        - "/bin/dash" # 150.46 KB
        - "/bin/sh" # Link to /bin/dash
...
```
---
## Take a closer look at each section: `packages`

```yaml
...
  - name: "fsl-5.0-core"
    version: "5.0.9-3~nd16.04+1"
    size: 39678976
    packfiles: true
    files:
      # Total files used: 2.33 MB
      # Installed package size: 37.84 MB
      - "/usr/lib/fsl/5.0" # Directory
      - "/usr/lib/fsl/5.0/bet" # 13.41 KB
      - "/usr/lib/fsl/5.0/bet2" # 71.14 KB
      - "/usr/lib/fsl/5.0/imtest" # 4.29 KB
      - "/usr/lib/fsl/5.0/libfslio.so" # 50.25 KB
      - "/usr/lib/fsl/5.0/libmeshclass.so" # 94.34 KB
      - "/usr/lib/fsl/5.0/libmiscmaths.so" # 571.57 KB
      - "/usr/lib/fsl/5.0/libnewimage.so" # 1.46 MB
      - "/usr/lib/fsl/5.0/libprob.so" # 31.66 KB
      - "/usr/lib/fsl/5.0/libutils.so" # 50.45 KB
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
  - "/etc/ld.so.cache" # 31.01 KB
  - "/lib64/ld-linux-x86-64.so.2" # Link to /lib/x86_64-linux-gnu/ld-2.23.so
  - "/src/workdir" # Directory
  - "/src/workdir/sub-01_T1w.nii.gz" # 13.07 MB
```
