from pssh import ParallelSSHClient
from flask import Flask, request
import yaml
import logging

# Globals
HOSTS = yaml.load('HOSTS.yml')
BOOTSTRAPPED = [] # Move to a db
WEBHOOK_QUEUE = queue.Queue(1000)
POOL = pool.Pool(4)

webhook_listener = Flask(__name__)
webhook_listener.config['PROPOGATE_EXCEPTION'] = True


@webhook_listener.route('/webhook', methods=['POST'])
def add_webhook_to_queue():
    post_data = request.get_json()
    logger.debug('received post data: {}'.format(post_data))
    response = []
    role_name, clone_url = post_data['repository']['name'], \
                           post_data['repository']['clone_url']
    servers, username, password = HOSTS[role_name]['servers'], \
                                  HOSTS[role_name]['username'], \
                                  HOSTS[role_name]['password']
    logger.info('Recieved webhook for repo {}'.format(clone_url))
    new_servers = [s for s in servers if s not in BOOTSTRAPPED]
    print('new servers {0}'.format(new_servers))
    if new_servers:
        output = bootstrap_servers(new_servers, username, password, role_name, clone_url)
        response.append(output)
        print(output)
    if role_was_modified(post_data):
        output = do_ssh_client(servers, role_name, clone_url, username, password)  # Returns a List
        response.append(output)
    return response, 200



@webhook_listener.route('/test', methods = ['GET'])
def test_api():
    return 'OK', 200


def do_ssh_client(servers, role_name, clone_url, username, password):
    command = 'python /src/{0}/toy-client.py {0}'.format(role_name)
    ssh_client = ParallelSSHClient(servers, user=username, password=password, pool_size=100)
    stdout = read_stdout(ssh_client.run_command('{}'.format(command), stop_on_errors=False))
    logger.info(stdout)
    return stdout


def read_stdout(output):
    # Todo: Make this capture and filter stdout all pretty-like
    response = ['stdout']
    for host in output:
        for line in output[host]['stdout']:
            r = 'Host {0} - {1}'.format(host, line)
            response.append(r)
    return response


def bootstrap_servers(servers, username, password, role_name, clone_url):
    logger.info('bootstrapping {}'.format(servers))
    logger.info('Bootstrapping servers: {0}'.format(servers))
    command = ''' if [ ! -f '/src/{0}/toy-client.py' ]; then apt-get install -y git python-pip libevent-dev \
            &&  mkdir -p /src ; cd /src; git clone {1}; \
            pip3 install -r '/src/{0}/requirements.txt'; fi'''.format(role_name, clone_url)
    try:
        ssh_client = ParallelSSHClient(servers, user=username, password=password, pool_size=100)
        output = read_stdout(ssh_client.run_command('{}'.format(command), stop_on_errors=True))
        BOOTSTRAPPED.append(servers)
    except Exception as e:
        print('Exception: {}'.format(e))


def role_was_modified(data):
    # Todo: test if modified files should trigger a run
    return True

def start_logging(verbose):
    logger = logging.getLogger('ToyDaemon')
    logging_filehandler = logging.FileHandler('/var/log/toy-daemon.log')
    logging_streamhandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logging_filehandler.setFormatter(formatter)
    logging_streamhandler.setFormatter(formatter)
    logger.addHandler(logging_filehandler)
    logger.addHandler(logging_streamhandler)
    logger.setLevel(logging.DEBUG) if verbose else logger.setLevel(logging.INFO)
    logger.info('-> Started logging')
    return logger

if __name__ == '__main__':
    verbose = False
    logger = start_logging(verbose)
    http_server = Flask(__name__)
    http_server.run(port=80)


