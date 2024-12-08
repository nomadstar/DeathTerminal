import threading
import time
import json
import comunicacion_bus as cb


def startservice(process_id):
    prefix = "Gen" + str(process_id)
    cb.register_service(prefix)


def run_daemon(number, function):
    while True:
        startservice(number)
        time.sleep(5)  # Sleep for 5 seconds
        if function is None:
            # end function and kill daemon
            break
        exec(open(function).read())
        time.sleep(5)
    #kill daemon

def main():
    daemon_thread = threading.Thread(target=run_daemon(1,None))
    daemon_thread.daemon = True  # Daemonize the thread
    daemon_thread.start()
    while True:
        time.sleep(1)  # Sleep for 1 second

if __name__ == "__main__":
    main()