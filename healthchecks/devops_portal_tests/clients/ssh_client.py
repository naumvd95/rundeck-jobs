import logging
import socket
import time

import paramiko
import six


from devops_portal_tests import exceptions

logger = logging.getLogger(__name__)


class SSHClient(object):

    def __init__(self, host, username, password=None, pkey=None,
                 port=22, timeout=300, channel_timeout=10):
        """SSH client

        :param host: str, host to login
        :param username: str, SSH username
        :param password: str, SSH password, or a password to unlock private key
        :param pkey: str, SSH private key
        :param port: str, SSH port
        :param timeout: int, timeout in seconds
        :param channel_timeout: Channel timeout in seconds, passed to the
            paramiko.  Default is 10 seconds.
        :return:
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.timeout = int(timeout)
        self.channel_timeout = int(channel_timeout)

        if isinstance(pkey, six.string_types):
            pkey = paramiko.RSAKey.from_private_key(six.StringIO(str(pkey)))
        self.pkey = pkey

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __del__(self):
        logger.debug('Close the all connections for {}@{}:{}'
                     .format(self.username, self.host, self.port))
        self.ssh.close()

    def _is_timed_out(self, start_time):
        return (time.time() - self.timeout) > start_time

    def _connect(self, delay=1):
        if self.pkey is not None:
            logger.debug('Creating ssh connection to {host}:{port} as {user}'
                         'with public key authentication'.format(
                             host=self.host,
                             port=self.port,
                             user=self.username))
        else:
            logger.debug('Creating ssh connection to {host}:{port} as {user}'
                         'with password authentication'.format(
                             host=self.host,
                             port=self.port,
                             user=self.username))

        attempts = 0
        _start_time = time.time()
        while True:
            try:
                self.ssh.connect(
                    self.host, port=self.port, username=self.username,
                    password=self.password,
                    timeout=self.channel_timeout, pkey=self.pkey)
                logger.debug('ssh connection to {}@{} successfully created'
                             .format(self.username, self.host))
                break
            except (EOFError,
                    socket.error, socket.timeout,
                    paramiko.SSHException) as exc:
                self.ssh.close()
                if self._is_timed_out(_start_time):
                    logger.exception('Failed to establish authenticated ssh'
                                     ' connection to {}@{} after {} attempts'
                                     .format(self.username, self.host,
                                             attempts))
                    raise exceptions.SSHTimeout(host=self.host,
                                                user=self.username,
                                                password=self.password)
                attempts += 1
                logger.warning('Failed to establish authenticated ssh'
                               ' connection to {}@{} ({}) after attempts: {}.'
                               ' Retry after {} seconds.'
                               .format(self.username, self.host, exc,
                                       attempts, delay))
                time.sleep(delay)

    def _check_connection(self):
        logger.debug('Check connection to {}@{}:{}'
                     .format(self.username, self.host, self.port))
        if self.ssh.get_transport() is None:
            self._connect()
        if self.ssh.get_transport().is_alive():
            return
        else:
            logger.warning('The current connection seems non-working.'
                           ' Try to reconnect.')
            self._reconnect()

    def _reconnect(self):
        logger.debug('Reconnect to {}@{}:{}. Close current connection'
                     .format(self.username, self.host, self.port))
        self.ssh.close()
        self._connect()

    def exec_command(self, cmd, check_exit_status=True):
        self._check_connection()
        transport = self.ssh.get_transport()
        with transport.open_session() as chan:
            stdin = chan.makefile('wb')
            stdout = chan.makefile('rb')
            stderr = chan.makefile_stderr('rb')
            cmd = "{}\n".format(cmd)
            chan.exec_command(cmd)
            stdout = stdout.read()
            stderr = stderr.read()

            exit_status = chan.recv_exit_status()
            logger.debug('The command {!r} was executed on {}@{}:{} with exit '
                         'code {}. Details:\n stdout: {},\nstderr: {}'
                         .format(cmd, self.username, self.host, self.port,
                                 exit_status, stdout, stderr))
            if check_exit_status:
                if exit_status != 0:
                    raise exceptions.SSHExecCommandFailed(
                        command=cmd, exit_status=exit_status, stderr=stderr,
                        stdout=stdout
                    )
        return chan, stdin, stdout, stderr
