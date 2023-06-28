from flask import Flask, render_template, request, redirect, url_for
from urllib.request import urlopen
import json
import requests
# from urllib2 import urlopen

app = Flask(__name__)

@app.route("/", methods =["GET", "POST"])
def home():
    domainName = ""
    WhoisService_result={}
    dns_result = {}
    ssl_result= {}
    msg =''

    if request.method == "POST":
        print("yes")
        # getting input with name = domain_name in HTML form
        domainName = request.form.get("domain_name")
        #    apiKey = 'at_e87tffSBDYarhfb5QwQ54cfUWTv41'   # office email id account
        apiKey = 'at_vsm0sf9T00GFB8NA72WZbmRvjX1Ty'   # personal email id account
        
        if  domainName:
            ''' Domain API '''  
            
            url = 'https://www.whoisxmlapi.com/whoisserver/WhoisService?' + 'domainName=' + domainName + '&apiKey=' + apiKey + "&outputFormat=JSON"
            response = urlopen(url)
            WhoisService_result = json.loads(response.read().decode('utf-8'))
            print("*********Domain API  OK")

            ''' DNS API '''
            dns_url = 'https://www.whoisxmlapi.com/whoisserver/DNSService?' + 'apiKey=' + apiKey + '&domainName=' + domainName + '&type=MX' + "&outputFormat=JSON"
            dns_response = urlopen(dns_url)
            dns_result = json.loads(dns_response.read().decode('utf-8'))
            print("*********DNS API  OK")  
            
            '''SSL API'''
            ssl_url = 'https://ssl-certificates.whoisxmlapi.com/api/v1?' + 'apiKey=' + apiKey + '&domainName=' + domainName + '&outputFormat=JSON' + '&withChain=0'
            ssl_response = urlopen(ssl_url)
            ssl_result = json.loads(ssl_response.read().decode('utf-8'))
            print("*********SSL API  OK") 

            
            
            """ Server"""
            try:
                _url = 'https://' + domainName
                response_ = requests.get(_url)
                if response_.status_code == 200:
                    msg = f"The website {_url} is up and running."
                    # print(f"The website {_url} is up and running.")
                else:
                    # print(f"The website {_url} is down with status code: {response_.status_code}")
                    msg = f"The website {_url} is down with status code: {response_.status_code}"
            except requests.ConnectionError:
                # print(f"The website {_url} is down.")
                msg = f"The website {_url} is down."
            print("*********Server API  OK") 

        # return render_template('home.html', WhoisService_result=WhoisService_result, dns_result = dns_result, ssl_result=ssl_result, domainName=domainName, msg = msg )
    return render_template('home.html', domainName=domainName, WhoisService_result=WhoisService_result, dns_result = dns_result, ssl_result=ssl_result, msg = msg)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=6549)