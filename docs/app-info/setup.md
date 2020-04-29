# Application Setup

Use `rails credentials:edit` to edit secrets.

Ask another dev for master.key file

for non secret / env variables, `cp config/settings.sample.yml config/settings.yml`

for database variables, `cp config/database.sample.yml config/database.yml`

Change the secrets for sso before deploying the application

## Server Requirements

#### software
* Pandoc
* Node
* Yarn
* Ruby
* Rails
* Bundler
* Email (sendmail)
* git-lfs
* samtools (1.5)
* bcftools (1.5)
* intel opencl runtime (16.1.1)
* cas-offinder (2.4)
* ncbi-blast (2.7.1+) -- *for: blastn*

#### python/pip prereqs
* biopython
* gffutils
* numpy
* scipy
* scikit-learn

#### database
* dev - sqlite3
* prod - sqlite3
  * for centos 7: compile from source, as in build docs
  * _`(Your version of SQLite (3.7.17) is too old. Active Record supports SQLite >= 3.8.)`_

## Git LFS

- installing on mac - `brew install git-lfs`
- run `git lfs install`
- run `git lfs fetch` to setup a project with LFS
- run `git lfs pull` to update files in vcfs directory
- `git lfs track` will display what files are using LFS
