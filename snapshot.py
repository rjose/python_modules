# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

import io
import os
import re
import subprocess
import zmq

from utils.sectionize import sectionize

class CommitError(Exception):
    pass

# TODO: Move this to sectionize
def make_sections(section_lists):
    sections = []
    for sls in section_lists:
        header = "=====%s\n" % sls[0]
        data = sls[1]
        sections.append(header + data)
    result = "".join(sections)
    return result

def get_sockets(section, config):
    host = config.get(section, 'host')
    req_port = int(config.get(section, 'request_port'))
    sub_port = int(config.get(section, 'subscribe_port'))

    context = zmq.Context()

    # Create request socket
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://%s:%d" % (host, req_port))

    # Create subscribe socket
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://%s:%d" % (host, sub_port))

    return [req_socket, sub_socket]

def construct_put_message(header, lines, options = {}):
    if 'add_newline' in options:
        join_char = "\n"
    else:
        join_char = ""
    header = "=====PUT %s\n" % header
    data = []
    for line in lines:
        data.append("\t%s" % line)
    message = header + join_char.join(data)
    return message

class SnapshotService:
    """Manages snapshotting data files"""

    #===========================================================================
    # Public API
    #

    #---------------------------------------------------------------------------
    # Sets up 0mq sockets and repo to use for snapshot data.
    #
    def __init__(self, header_file_map, repo_dir, reply_port, publish_port):
        self.header_file_map = header_file_map
        context = zmq.Context()

        # Socket for replying to snapshot requests from users (GETs and PUTs)
        self.rep_socket = context.socket(zmq.REP)
        self.rep_socket.bind("tcp://127.0.0.1:%d" % reply_port)
        
        # Socket for publishing changes to resources
        self.pub_socket = context.socket(zmq.PUB)
        self.pub_socket.bind("tcp://127.0.0.1:%d" % publish_port)

        # Set working directory to the repo
        os.chdir(repo_dir)


    #---------------------------------------------------------------------------
    # Event loop for handling snapshot PUT/GET requests.
    #
    def run(self):
        while True:
            try:
                message = io.StringIO(self.rep_socket.recv())
                sections = sectionize(message)
        
                for header in sections.keys():
                    if re.match("PUT", header):
                        self.put_resource(header, sections[header], self.header_file_map)
                    elif re.match("GET", header):
                        self.get_resource(header, sections[header], self.header_file_map)
                    else:
                        print("TODO: Handle: %s" % header)
                        self.rep_socket.send_unicode("TODO: Handle %s" % header)
            except Exception as e:
                print("EXCEPTION: %s" % str(e))
                self.rep_socket.send_unicode("ERROR: %s" % str(e))


    #===========================================================================
    # Internal functions
    #

    #---------------------------------------------------------------------------
    # Wraps git to commit data to repo.
    #
    def commit_file(self, file):
        # Add file
        git_result = subprocess.call("git add %s" % file, shell=True)
        if git_result != 0:
            raise CommitError("Problem adding %s" % file)
    
        # Commit file
        git_result = subprocess.call("git commit -m 'Update %s'" % file, shell=True)
    
        # TODO: Check if file hasn't changed
        #if git_result != 0:
        #    socket.send("ERROR: Couldn't commit raw/qplan.txt")
        #    raise Exception("Problem commiting raw/qplan.txt")


    #---------------------------------------------------------------------------
    # Writes a new data snapshot to database.
    #
    def put_resource(self, header, data, header_map):
        resource = header.split("PUT ")[1]
        filename = header_map[resource]
        dirname = os.path.dirname(filename)
        # TODO: Test this at least once
        if not (os.path.exists(dirname) or dirname == ""):
            os.makedirs(dirname)
    
        # Write data to file
        file = open(filename, "w")
        file.write(data);
        file.close()
    
        # Check file in
        try:
            self.commit_file(filename)
    
            # Publish that file was checked in
            self.pub_socket.send_unicode("=====%s" % resource);
    
            # Reply to client that PUT file
            self.rep_socket.send("OK")
        except CommitError:
            self.rep_socket.send_unicode("ERROR: Couldn't commit PUT %s" % resource)
    
    

    #---------------------------------------------------------------------------
    # Retrieves data snapshot.
    #
    def get_resource(self, header, data, header_map):
        try:
            resource = header.split("GET ")[1]
            filename = header_map[resource]
            version = data.split("\t")[0]
            if not version:
                version = "HEAD"
            print("Getting data for %s, %s" % (header, version))
    
            p = subprocess.Popen("git show %s:%s" % (version, filename),
                    stdout=subprocess.PIPE, shell=True)
            contents = io.StringIO(p.communicate()[0])
    
            p = subprocess.Popen("git rev-parse %s" % version,
                    stdout=subprocess.PIPE, shell=True)
            rev = p.communicate()[0][0:5]
    
            data = []
            for l in contents.readlines():
                data.append("\t%s" % l)
            new_contents = "".join(data)
            message = make_sections([[resource, "\t%s\n" % rev], ["data", new_contents]])

            self.rep_socket.send_unicode(message)
        except:
            self.rep_socket.send_unicode("ERROR: Couldn't GET %s @ %s" % (resource, version))
