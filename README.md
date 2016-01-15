# toy-config
A small implementation of an ansible-like configuration tool
There are two main components: toy_client and toy_daemon.


### toy_daemon: Flask service triggered by github webhooks.

It scrapes the JSON post data for the repo name which should be the same as the role of the
services configured by the runbook in that repo. A hosts file is then consulted to get a list of servers
assosciated with that role. Unless that host is listed in a list called "BOOTSTRAPED", toy_daemon
connects to each host over ssh and runs shell commands to pull down the toy_config repo and install
a few python requirements.

Once servers are listed as "BOOTSTRAPPED" it will use parallel-ssh to trigger a "toy-config --role rolename"
on each host.


### toy_config: Script to copy configuration files to local host and run shell commands.

The runbook is expected to live in a git repository of the same name as the role. First, that repo is cloned
(or pulled if it already exists) to the local filesystem. Then a file called runbook.yml is parsed for a list of
tasks and template variables aka attributes. Each task is fed to the TaskHandler.handle_task() method serially.
Tasks either execute a shell command or cause a file to be written to the local filesystem.
Using the 'files' task, files of any kind are copied from the /files directory of the repo to a specified destination.
Using the 'templates' task, a jinja2 template is rendered using variables passed in as a dict called 'attributes'

### TaskHandler: A class used by toy_client which contains all the host-altering actions described in run

### ToDo: toy_daemon could be cleaned up a lot. I didn't get gevent queues all the way working.
# ToDo: a way for attributes to be overriden on the role level so that runbooks are more generic
# ToDo: better exception handling. I did some hacky things to make the toy_client exit in a shell-friendly way.
# ToDo: Incremental updates. Either pass a list of files altered from github webhook or locally compare commits.
# ToDo: Write a test harness. Unit tests are insufficient for