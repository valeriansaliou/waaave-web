#!/bin/sh
# -*- coding: utf-8 -*- 
''''exec python2 -- "$0" ${1+"$@"} # '''

#############
#### RUN ####
#############

# Note: used for all environments to automate application run process
# Settings are changed in Django website settings

import sys, os, signal, pty, subprocess, re, time, psutil
import _settings


# Go to project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
os.chdir(BASE_DIR)


# Run configuration
MODULE_NS = "run"

SLEEP = 0.1

SOCKETS_DIR = "./tmp/sockets/"
PIDS_DIR = "./tmp/pids/"
LOGS_DIR = "./log/"


# Run initialization
PID_REGEX = re.compile(r'(.*)\.pid$')

MASTER, SLAVE = pty.openpty()
PROCESSES = []



class Colors(object):
    """
    Map colors for terminal
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKYELLOW = '\033[33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


    @classmethod
    def disable(_class):
        """
        Disable all colors
        """
        _class.HEADER = ''
        _class.OKBLUE = ''
        _class.OKGREEN = ''
        _class.OKYELLOW = ''
        _class.WARNING = ''
        _class.FAIL = ''
        _class.ENDC = ''



class Socket(object):
    """
    Socket operations
    """

    @staticmethod
    def path(ns):
        """
        Return socket absolute path
        """
        assert type(ns) is str and ns != ''

        return os.path.abspath(os.path.join(SOCKETS_DIR, '%s.sock' % ns))



class PID(object):
    """
    PID operations
    """

    @staticmethod
    def path(ns):
        """
        Return PID absolute path
        """
        assert type(ns) is str and ns != ''

        return os.path.abspath(os.path.join(PIDS_DIR, '%s.pid' % ns))


    @classmethod
    def save(_class, ns, pid):
        """
        Save PID
        """
        assert type(ns) is str and ns != ''
        assert type(pid) is str or int and str(pid) != ''

        file_pid = open(_class.path(ns), 'w+')
        file_pid.write(str(pid))
        file_pid.close()


    @classmethod
    def read(_class, ns):
        """
        Read PID
        """
        assert type(ns) is str and ns != ''

        value_pid = None

        try:
            value_pid = ''
            with open(_class.path(ns), 'r') as content_file:
                value_pid = value_pid + content_file.read()
            value_pid = value_pid.strip()
            if value_pid.isdigit():
                value_pid = int(value_pid)
            else:
                value_pid = None
        except IOError:
            pass
        finally:
            return value_pid


    @staticmethod
    def kill(pid, signal=signal.SIGTERM):
        """
        Kill a PID tree
        """
        try:
            pid_children = psutil.Process(pid).get_children(recursive=True)
            os.kill(pid, signal)

            for cur_pid_child in pid_children:
                try:
                    os.kill(cur_pid_child.pid, signal)
                except OSError:
                    pass
            return True
        except (psutil.NoSuchProcess, OSError):
            return False


    @classmethod
    def remove(_class, ns):
        """
        Remove PID
        """
        assert type(ns) is str and ns != ''

        os.remove(_class.path(ns))



class Log(object):
    """
    Log operations
    """

    @staticmethod
    def path(ns):
        """
        Return socket absolute path
        """
        assert type(ns) is str and ns != ''

        return os.path.abspath(os.path.join(LOGS_DIR, '%s.log' % ns))



class Daemon(object):
    """
    Daemon operations
    """

    @staticmethod
    def run():
        """
        Run daemon
        """
        print("--(%s)[DAEMON:RUN:WAIT]--" % MODULE_NS)

        Run.start()

        print(Colors.OKGREEN + ("--(%s)[DAEMON:RUN:DONE]--" % MODULE_NS) + Colors.ENDC)


    @staticmethod
    def fork(command, stdout=False, stderr=False, shell=False):
        """
        Fork a new daemon sub-process (given a command)
        """
        assert type(command) is str

        process = subprocess.Popen(
            command.split(),
            stdin=subprocess.PIPE,
            stdout=SLAVE if not stdout else subprocess.PIPE,
            stderr=SLAVE if not stderr else subprocess.PIPE,
            shell=shell,
            cwd=BASE_DIR,
        )
        PROCESSES.append(process)

        return process


    @classmethod
    def init_fork(_class, command, pid_file, save_pid_file=True, stdout=False, stderr=False, shell=False):
        """
        Initialize a daemon fork
        """
        pid = PID.read(pid_file)
        pid_running = False

        if pid:
            pid_running = True
            try:
                os.kill(pid, 0)
            except OSError:
                print(Colors.WARNING + (" Zombie PID found, starting anyway.") + Colors.ENDC)
                pid_running = False

        if not pid_running:
            print(Colors.OKBLUE + (" %s" % command) + Colors.ENDC)
            process = _class.fork(command, stdout=stdout, stderr=stderr, shell=shell)

            if save_pid_file:
                PID.save(pid_file, process.pid)
        else:
            print(Colors.OKBLUE + (" Already running.") + Colors.ENDC)


    @staticmethod
    def unfork(pid, pid_file, signal=signal.SIGTERM):
        """
        Unfork a daemon
        """
        PID.remove(pid_file)
        return PID.kill(pid, signal)


    @classmethod
    def signals(_class):
        """
        Handle daemon signals
        """
        signal.signal(signal.SIGTERM, _class.terminate)

        for cur_signal in (signal.SIGABRT,signal.SIGILL,signal.SIGINT,signal.SIGSEGV,):
            signal.signal(cur_signal, _class.kill)


    @staticmethod
    def health():
        """
        Grab the global return code of all running childs
        """
        return_code = 0

        for cur_process in PROCESSES:
            if not cur_process.returncode: continue
            
            if cur_process.returncode > return_code:
                return_code = cur_process.returncode

        return return_code


    @staticmethod
    def kill(*args, **kwargs):
        """
        Kill the running daemon
        """
        print("--(%s)[DAEMON:KILL:WAIT]--" % MODULE_NS)

        Run.stop(signal.SIGKILL)

        print(Colors.OKGREEN + ("--(%s)[DAEMON:KILL:DONE]--" % MODULE_NS) + Colors.ENDC)


    @staticmethod
    def terminate(*args, **kwargs):
        """
        Terminate the running daemon
        """
        print("--(%s)[DAEMON:TERMINATE:WAIT]--" % MODULE_NS)

        Run.stop(signal.SIGTERM)

        print(Colors.OKGREEN + ("--(%s)[DAEMON:TERMINATE:DONE]--" % MODULE_NS) + Colors.ENDC)



class Run(object):
    """
    Run operations
    """

    @staticmethod
    def start():
        """
        Start run tasks
        """
        for cur_run_task_reg in _settings.RUN:
            cur_run_task_name = cur_run_task_reg[0]

            for cur_run_task_sub_reg in cur_run_task_reg[1]:
                cur_run_task_task = cur_run_task_sub_reg[0]
                cur_run_task_command = cur_run_task_sub_reg[1]
                
                cur_run_task_ns = "%s:%s" % (cur_run_task_name,cur_run_task_task,)

                cur_pid_file = "%s_%s" % (cur_run_task_name,cur_run_task_task,)
                cur_socket_file = cur_pid_file
                cur_log_file = cur_pid_file

                if cur_run_task_command:
                    print("\n--(%s)[TASK:START:WAIT:%s]--" % (MODULE_NS,cur_run_task_ns,))

                    cur_save_pid_file = True

                    if '{pid_file}' in cur_run_task_command\
                       or '{socket_file}' in cur_run_task_command\
                       or '{log_file}' in cur_run_task_command:
                        cur_save_pid_file = not '{pid_file}' in cur_run_task_command
                        cur_run_task_command = cur_run_task_command.format(
                            pid_file=PID.path(cur_pid_file),
                            socket_file=Socket.path(cur_socket_file),
                            log_file=Log.path(cur_log_file),
                        )

                    Daemon.init_fork(cur_run_task_command, cur_pid_file, save_pid_file=cur_save_pid_file, stdout=True, stderr=True)

                    print(Colors.OKGREEN + ("--(%s)[TASK:START:DONE:%s]--\n" % (MODULE_NS,cur_run_task_ns,)) + Colors.ENDC)
                else:
                    print(Colors.WARNING + ("--(%s)[TASK:START:PASS:%s]--\n" % (MODULE_NS,cur_run_task_ns,)) + Colors.ENDC)


    @staticmethod
    def stop(signal=signal.SIGTERM):
        """
        Stop run tasks
        """
        all_pids = []

        for cur_dir in os.listdir(PIDS_DIR):
            cur_match = PID_REGEX.match(cur_dir)
            if cur_match:
                all_pids.append(cur_match.group(1))

        for cur_pid_file in all_pids:
            print("\n--(%s)[TASK:STOP:WAIT:%s]--" % (MODULE_NS,cur_pid_file,))

            cur_pid = PID.read(cur_pid_file)
            if cur_pid:
                if Daemon.unfork(cur_pid, cur_pid_file, signal):
                    print(Colors.OKBLUE + (" PID removed, process stopped (%s)" % cur_pid_file) + Colors.ENDC)
                else:
                    print(Colors.FAIL + (" Process could not be stopped, maybe zombie? (%s)" % cur_pid_file) + Colors.ENDC)
            else:
                print(Colors.OKBLUE + (" No PID found, nothing done (%s)" % cur_pid_file) + Colors.ENDC)

            print(Colors.OKGREEN + ("--(%s)[TASK:STOP:DONE:%s]--\n" % (MODULE_NS,cur_pid_file,)) + Colors.ENDC)



if __name__ == "__main__":
    if len(sys.argv) <= 1:
        Daemon.signals()
        Daemon.run()

        if Daemon.health() is 0:
            print(Colors.OKGREEN + ("\nWaaave now running. Ready to party?") + Colors.ENDC)
            print(Colors.OKYELLOW + ("\nTo gracefully stop all services, use {terminate}") + Colors.ENDC)
            print(Colors.OKYELLOW + ("Hardcore guys might rather prefer {kill}") + Colors.ENDC)
        else:
            print(Colors.FAIL + ("\nWaaave could not start. Please check the startup log above") + Colors.ENDC)
            print(Colors.WARNING + ("Warning: some services might have started, though") + Colors.ENDC)
    else:
        if sys.argv[1] == 'kill':
            Daemon.kill()
            print(Colors.OKYELLOW + ("\nWaaave killed. What an hangover!") + Colors.ENDC)
        elif sys.argv[1] == 'terminate':
            Daemon.terminate()
            print(Colors.OKYELLOW + ("\nWaaave now stopped. The party is over!") + Colors.ENDC)
            print(Colors.WARNING + ("\nWarning: terminate might not have stopped all processes correctly (some restart after receiving SIGTERM)") + Colors.ENDC)
        else:
            print("Usage: {kill, terminate} or no argument to start")

    print("\nRun done (environment: %s)" % _settings.ENVIRONMENT)

    # Exit with proper return code
    sys.exit(Daemon.health())
else:
    raise Exception("This script must be ran alone, since it will daemonize itself.")