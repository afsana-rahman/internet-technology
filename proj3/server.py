import socket
import signal
import sys
import random

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)
host = socket.gethostname()
# print(socket.gethostbyname(host))


### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    print("Here is the", tag)
    print("\"\"\"")
    print(value)
    print("\"\"\"")
    print()

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# Read login credentials for all the users
lines = []
with open('passwords.txt', 'r') as f:
    lines = f.readlines()
credentials = {}
for line in lines:
    tokens = line.strip().split(' ')
    credentials[tokens[0]] = tokens[1]

##################################
### BEGIN STUDENT CONTRIBUTION ###
##################################
# Read secret data of all the users
lines = []
with open('secrets.txt', 'r') as f:
    lines = f.readlines()
secrets = {}
for line in lines:
    tokens = line.strip().split(' ')
    secrets[tokens[0]] = tokens[1]

cookies = {}

### Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024)

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)

    headers_to_send = ''

    if body != '':
        if "action=logout" in body:
            value = headers.split("token=", 1)[1]
            value = value.split("Content", 1)[0].strip()
            del cookies[value]
            html_content_to_send = logout_page

        # check for cookies
        elif "Cookie" in headers:
            value = headers.split("token=", 1)[1]
            value = value.split("Content", 1)[0].strip()
            if value in cookies.keys():
                # valid cookie
                html_content_to_send = success_page + secrets.get(cookies[value])
            else:
                # invalid cookie
                html_content_to_send = bad_creds_page

        # no cookies: check the login credentials
        else:
            authen = body.split('&')
            username = authen[0].split('=')[1]
            password = authen[1].split('=')[1]
            
            if len(username) == 0 or len(password) == 0:
                # username or password not entered
                html_content_to_send = bad_creds_page
            else:
                if username in credentials.keys() and credentials[username] == password:
                    # valid username and password
                    html_content_to_send = success_page + secrets[username]
                    rand_val = str(random.getrandbits(64))
                    headers_to_send = 'Set-Cookie: token=' + rand_val + '\r\n'
                    cookies[rand_val] = username
                else:
                    # invalid username or password
                    html_content_to_send = bad_creds_page

    else:
        html_content_to_send = login_page

    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response)
    client.close()
##################################
#### END STUDENT CONTRIBUTION ####
##################################
    
    print("Served one request/connection!")
    print

# We will never actually get here.
# Close the listening socket
sock.close()
