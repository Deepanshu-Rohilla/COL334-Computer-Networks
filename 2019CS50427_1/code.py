import subprocess
import sys
import matplotlib.pyplot as plt


def plot(x,y,domain):
    plt.plot(x, y, color='green', linestyle='dashed', linewidth = 3,
         marker='o', markerfacecolor='blue', markersize=12)
    plt.xlabel('Hops')
    plt.ylabel('RTT (in seconds)')
    title = "Output Graph " + domain
    plt.title(title)
    plt.savefig('plot.png')
    plt.show()
    


def f(domain):
    y_axis = []
    x_axis = []
    x1 = subprocess.run(['nslookup',domain], capture_output=True , text = True)
    ipList = x1.stdout.split(" ")
    if(ipList[-1]=="NXDOMAIN\n\n"):
        print("Incorrect domain name. Please enter a valid domain name.")
        return
    ipString = ipList[-1][:-2]
    print("Running the code for: ", end = "")
    print(domain)
    print ("{:<20} {:<20} {:<20}".format('Hops', 'IP Address', 'RTT'))
    for i in range(1,61):
        temp = subprocess.run(['ping','-c', '1', '-m',str(i), ipString],capture_output=True , text = True)
        x_axis.append(i)
        # print(temp.stdout)
        tempL = temp.stdout.split(" ")
        ipAddr = ""
        rtt = 0
        tempLine = temp.stdout.split("\n")[1].split(" ")
        index = tempLine.index('from')
        if(tempLine[index+1][1].isnumeric()):
            ipAddr = tempLine[index+1][:-1]
        else:
            ipAddr = tempLine[index+2][1:-2]

        # print(ipAddr)
        decider = tempL[-1]
        if(decider!='loss\n'):
            rtt = temp.stdout.split("\n")[1].split(" ")[-2].split('=')[1]
            y_axis.append(rtt)
            break
        else:
            ping1 = subprocess.run(['ping','-c', '1', ipAddr],capture_output=True , text = True)
            # print(ping1.stdout)
            try:
                rtt = ping1.stdout.split("\n")[1].split(" ")[-2].split('=')[1]
                y_axis.append(rtt)
            except:
                rtt = 0.00
                y_axis.append(rtt)
        print ("{:<20} {:<20} {:<20}".format(i, ipAddr, rtt))
    print("Reached the destination!!!")
    plot(x_axis,y_axis,domain)
          

 
if __name__ == "__main__":
    try:
        domain = str(sys.argv[1])
        f(domain)
    except IndexError as i:
        print("Enter domain name")
        