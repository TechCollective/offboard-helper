# Manage Google Workspace data

## Notes
This project is designed to bascily run GYB (Got Your Back) in batch mode. So you can que up a bunch of 
GYB jobs and have the run one after the other.

Just install and run the script. It will ask you a few questions, then run all the runs.

## TODO/ Roadmap
* Notifications - to email, a slack channel, or an Autotask Ticket
* add GAM support
  * create the group for the backup for you.
  * change the name of the user we are backing up and add an alias to whoever is suppose to get the new emails
* add RClown support - move the archive to a Google Shared Drive for you.
* Report - After the project runs all jobs, we should generate a report that explains everything for the client.
  * Did we get a full backup. 
  * For Group restore, did we reacht he Group upload limit, if so, how far did we get.
* Job Log - add a log file for each project that has the commands being run and the output of those commands. As well as anything relavant.
* I need to write up a guild on how to setup a Slackbot. 

## Slack Integration
Add you Slack Token to your .env file

TechCollective's setup uses Autotask and Tasky, which creates Slack channels based on the ticket number. When the scrip asks uif you want Slack notifications, it assumes it will find a channel based on the ticket number. Maybe I'll generalize this in the future. Once it find the channel, it joins it and then adds a message. It will send all new status updates as a thread to that message so it doesn't overwhelm the Slack Channel.

## Cement Notes
Below was created by the script builder I used called Cement. Below is it's default output for a README file. I have not veted any of the information below yet. I'll try to update it once I have something stable.

I have not tested Docker, it was created by cement.


## Installation

```
$ pip install -r requirements.txt

$ python setup.py install
```

## Development

This project includes a number of helpers in the `Makefile` to streamline common development tasks.

### Environment Setup

The following demonstrates setting up and working with a development environment:

```
### create a virtualenv for development

$ make virtualenv

$ source env/bin/activate


### run offboardhelper cli application

$ offboardhelper --help


### run pytest / coverage

$ make test
```


### Releasing to PyPi

Before releasing to PyPi, you must configure your login credentials:

**~/.pypirc**:

```
[pypi]
username = YOUR_USERNAME
password = YOUR_PASSWORD
```

Then use the included helper function via the `Makefile`:

```
$ make dist

$ make dist-upload
```

## Deployments

### Docker

Included is a basic `Dockerfile` for building and distributing `Offboard Helper`,
and can be built with the included `make` helper:

```
$ make docker

$ docker run -it offboardhelper --help
```
