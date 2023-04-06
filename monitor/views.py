import datetime
from django.shortcuts import render
import requests
import ping3
import os
import subprocess
import re
from django.http import HttpResponse
from speedtest_cli import Speedtest
import plotly.graph_objs as go
from plotly.offline import plot
def home(request):
    return render(request, 'home.html')
    

def speed_test(request):
    servers = [ '10.100.0.246','10.100.0.143']
    response_times = {}
    for server in servers:
        try:
            response = requests.get(server)
            response_times[server] = {
                'status': 'Active',
                'response_time': response.elapsed.total_seconds()
            }
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
            response_times[server] = {
                'status': 'Inactive',
                'response_time': 'N/A'
            }
    
    # Perform speed tests
    st = Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1000000  # convert bytes to megabits
    upload_speed = st.upload() / 1000000  # convert bytes to megabits
    
    return render(request, 'speed_test.html', {'response_times': response_times,'download_speed': round(download_speed, 2),'upload_speed': round(upload_speed, 2)})

def check_iis_uptime(request):
    server_urls = ["https://www.iis.net/", "https://www.microsoft.com/", "https://www.stackoverflow.com/"]
    server_statuses = []
    for server_url in server_urls:
        iis_response = requests.get(server_url)
        if iis_response.status_code == 200:
            iis_status = "active"
            last_updated = datetime.datetime.now()
        else:
            iis_status = "inactive"
            last_updated = None
        server_status = {"server_url": server_url, "iis_status": iis_status, "last_updated": last_updated}
        server_statuses.append(server_status)
    context = {"server_statuses": server_statuses}
    return render(request, "iis_uptime.html", context)

def ping_servers(request):
    servers = ["google.com", "facebook.com", "twitter.com"]
    results = []
    for server in servers:
        response_time = ping3.ping(server)
        if response_time is not None:
            status = "active"
            results.append({"server": server, "response_time": response_time, "status": status})
        else:
            status = "inactive"
            results.append({"server": server, "response_time": "Failed", "status": status})
    context = {"results": results}
    return render(request, "ping_servers.html", context)  

def check_mysql_service(request, *endpoints):
    if not endpoints:
        endpoints = ["http://10.110.0.36:8084", "http://10.110.0.34:8059","https://www.microsoft.com/"]
    endpoint_statuses = {}
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            endpoint_statuses[endpoint] = "up"
        except:
            endpoint_statuses[endpoint] = "down"
    active_endpoints = [endpoint for endpoint, status in endpoint_statuses.items() if status == "up"]
    if active_endpoints:
        result = f"MySQL service is up and running on {', '.join(active_endpoints)}."
        status = "active"
    else:
        result = "MySQL service is down."
        status = "inactive"
    context = {
        "result": result,
        "status": status,
        "endpoints": endpoint_statuses
    }
    return render(request, "check_mysql_service.html", context)

def ping_mno_links(request):
    mno_links = ["https://en.wikipedia.org/wiki/Safaricom", "https://en.wikipedia.org/wiki/Airtel", "https://en.wikipedia.org/wiki/Telkom_Kenya"]
    ping_results = []
    for link in mno_links:
        response_time = ping3.ping(link.replace("https://", ""))
        if response_time is not None:
            try:
                status_code = requests.get(link).status_code
                if status_code == 200:
                    status = "active"
                else:
                    status = "inactive"
            except:
                status = "inactive"
            ping_results.append({"link": link, "response_time": f"{response_time:.2f} ms", "status": status})
        else:
            ping_results.append({"link": link, "response_time": "Ping failed.", "status": "inactive"})
    context = {"ping_results": ping_results}
    return render(request, "ping_mno_links.html", context)

def ping_national_switch(request):
    national_switch_ip = "https://www.wikihow.com/Ping-an-IP-Address"
    national_switch_response_time = ping3.ping(national_switch_ip)
    if national_switch_response_time is not None:
        response_time = f"{national_switch_response_time:.2f} ms"
        status = "active"
    else:
        response_time = "Ping failed."
        status = "inactive"
    context = {"national_switch_ip": national_switch_ip, "response_time": response_time, "status": status}
    return render(request, "ping_national_switch.html", context)

def check_mx_record(request, mx_record):
    try:
        mx_response = subprocess.check_output(["nslookup", "-type=mx", mx_record]).decode("utf-8")
        mx_ip_match = re.search(r"mail exchanger = ([^\s]+)", mx_response)
        if mx_ip_match:
            mx_ip = mx_ip_match.group(1)
            try:
                mx_response_time = ping3.ping(mx_ip)
                if mx_response_time is not None:
                    response_time = f"{mx_response_time:.2f} ms"
                    status = "active"
                else:
                    response_time = "Ping failed."
                    status = "inactive"
            except:
                response_time = "Ping failed."
                status = "inactive"
        else:
            response_time = f"Unable to get MX record for {mx_record}."
            status = "inactive"
    except:
        response_time = f"Unable to get MX record for {mx_record}."
        status = "inactive"
    context = {"mx_record": mx_record, "response_time": response_time, "status": status}
    return render(request, "check_mx_record.html", context)

# def speed_test(request):
#     servers = ['10.100.0.246','10.100.0.243']
#     response_times = {}
#     for server in servers:
#         try:
#             response = requests.get(server)
#             response_times[server] = {
#                 'status': 'Active',
#                 'response_time': response.elapsed.total_seconds()
#             }
#         except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
#             response_times[server] = {
#                 'status': 'Inactive',
#                 'response_time': 'N/A'
#             }

#     # Perform speed tests
#     st = Speedtest()
#     st.get_best_server()
#     download_speed = st.download() / 1000000  # convert bytes to megabits
#     upload_speed = st.upload() / 1000000  # convert bytes to megabits

#     # Create a bar chart of the response times
#     response_time_data = go.Bar(
#         x=[server for server in response_times],
#         y=[response_times[server]['response_time'] for server in response_times],
#         name='Response Time',
#         marker=dict(color='blue')
#     )

#     # Create a pie chart of the server statuses
#     active_servers = len([server for server in response_times if response_times[server]['status'] == 'Active'])
#     inactive_servers = len(servers) - active_servers
#     server_status_data = go.Pie(
#         labels=['Active', 'Inactive'],
#         values=[active_servers, inactive_servers],
#         name='Server Status',
#         marker=dict(colors=['green', 'red'])
#     )

#     # Create a bar chart of the download and upload speeds
#     speed_data = go.Bar(
#         x=['Download', 'Upload'],
#         y=[download_speed, upload_speed],
#         name='Speed',
#         marker=dict(color='orange')
#     )

#     # Combine the plots into a single figure
#     fig = go.Figure(data=[response_time_data, server_status_data, speed_data])
#     fig.update_layout(title='Speed Test Results')

#     # Render the plot in the template
#     plot_div = plot(fig, output_type='div')

#     # Add real-time function
#     script = '''
#         setInterval(function() {
#             $.ajax({
#                 url: window.location.href,
#                 type: 'GET',
#                 success: function(data) {
#                     $('#plot_div').html($(data).find('#plot_div').html());
#                 }
#             });
#         }, 5000); // refresh every 5 seconds
#     '''

#     return render(request, 'speed_test.html', {'plot_div': plot_div, 'script': script})