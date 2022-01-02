import random
import string
import requests
import json
from datetime import datetime, timedelta
import time
from tqdm import tqdm
from multiprocessing import Process


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class Session:
    seshID = None
    #url = 'https://lather.fpay.cz'
    url = 'https://pay.fpay.cz/testing/service/index.php'
    headers = {'Content-type': 'application/json'}
    requestID = 1

    user = 'vcKZQtT96QUG3EW7yer1a2GHSwTIv6yBO5rZZLTYgf6UD6ll3wGb9WBiUUO3mrpluXmXGB3OZ6DRowUQzVkhnf4NMtWvhWL7cjIE'
    pass_ = 'hu53pxeOOMfDyIIlWFgTdecNmshp8kEtxwHnMkQ14RjjI3Kf9ihDTTo5R9drOgzAqhb1lY53sRFZgiSApLyEiZIiKRO0sAjY6gjc'

    logindata = {"method": "generalQuery",
                 "id": "1",
                 "params": ["", "login", {
                     "DeviceUsed": {"type": "string", "value": None},
                     "login": {"type": "string", "value": None},
                     "pass": {"type": "string", "value": None},
                     "IP": {"type": "string", "value": None},
                     "BrowserOrSoftwareUsed": {"type": "string", "value": "soap API"}
                 }]}

    def __init__(self, apiclient, user, passw, ip='127.0.0.1'):
        # init rID
        self.requestID = 1
        # assign fields
        self.logindata['params'][2]['DeviceUsed']['value'] = 'catchystring'#apiclient
        self.logindata['params'][2]['login']['value'] = user
        self.logindata['params'][2]['pass']['value'] = passw
        self.logindata['params'][2]['IP']['value'] = ip
        # POSTing to init the session (login request)
        r = requests.post(self.url, json=self.logindata, headers=self.headers, auth=(self.user, self.pass_))
        if r.status_code == 200:
            session = json.loads(r.text)
            self.seshID = session['result'][0][0]['sessionid']
        else:
            print(r.text)
        # if 'OTP' in json.loads(r.text)['result'][0][0]['message']:
        #     otpStr = input('Enter OTP:')
        #     otpLoginData = {"method": "generalQuery",
        #                     "id": "2",
        #                     "params": [self.seshID, "second_login", {
        #                         "value": {"type": "string", "value": otpStr},
        #                         "IP": {"type": "string", "value": ip}
        #                     }]}
        #     r = requests.post(self.url, json=otpLoginData, headers=self.headers, auth=(self.user, self.pass_))
        #     self.seshID = json.loads(r.text)['result'][1][0]['sessionid']

    def getEnums(self, doctype, docid, operation):
        enums = {}
        # if docid == '0':
        #     docid = None
        method = 'getMethodMetadata'
        payload = {"method": method,
                   "id": self.requestID,
                   "params": [self.seshID, doctype, docid, operation]}
        r = requests.post(self.url, json=payload, headers=self.headers, auth=(self.user, self.pass_))
        self.requestID += 1
        if 'session.wrong' in r.text:
            scode = 401
        else:
            metajson = json.loads(r.text)
            for el in metajson['result']['pages']:
                for gr in el['groups']:
                    for field in gr['fields']:
                        if field['required'] == 1:
                            if field['type'] == 'drop-down box':
                                enums[field['name']] = field['options']
        return enums

    def getDocExt(self, id):
        method = 'getDocument'
        doctype = 'Outgoing_Payment_FReq'
        payload = {"method": method,
                   "id": self.requestID,
                   "params": [self.seshID, doctype, id]
                   }
        r = requests.post(self.url, json=payload, headers=self.headers, auth=(self.user, self.pass_))
        self.requestID += 1
        return (json.loads(r.text))['result']

    def getSignReqs(self, id):
        # get sign method of last doc
        doc = self.getDocExt(id)
        signMeth = next((m for m in doc['methods'] if m['caption'] == 'Sign'), None)
        return str(signMeth['signaturetype']) + str(signMeth['signaturetype2'])

    def getCountries(self, doctype, docid, operation):
        method = 'getMethodMetadata'
        payload = {"method": method,
                   "id": self.requestID,
                   "params": [self.seshID, doctype, docid, operation]}
        r = requests.post(self.url, json=payload, headers=self.headers, auth=(self.user, self.pass_))
        self.requestID += 1
        if 'session.wrong' in r.text:
            scode = 401
        else:
            metajson = json.loads(r.text)
            for el in metajson['result']['pages']:
                for gr in el['groups']:
                    for field in gr['fields']:
                        if field['required'] == 1:
                            if field['name'] == 'benefcountry':
                                return field['options']

    def getCurrencies(self):
        method = 'getCurrencyInfo'
        payload = {"method": method,
                   "id": self.requestID,
                   "params": [self.seshID]}
        r = requests.post(self.url, json=payload, headers=self.headers, auth=(self.user, self.pass_))
        self.requestID += 1
        return (json.loads(r.text))['result']

    def getAccounts(self):
        method = 'getAccounts'
        payload = {"method": method,
                   "id": self.requestID,
                   "params": [self.seshID]}
        with open('/home/tumanenko/fpay/lather/getAcc.json', 'w') as jsonnn:
            json.dump(payload, jsonnn)
        r = requests.post(self.url, json=payload, headers=self.headers, auth=(self.user, self.pass_))
        self.requestID += 1
        return (json.loads(r.text))['result']

    def getBalance(self, accId, currId=2):
        method = 'getBalance'
        payload = {"method": method,
                   "id": self.requestID,
                   "params": [self.seshID, 3610, currId]}
        with open('/home/tumanenko/fpay/lather/getAcc.json', 'w') as jsonnn:
            json.dump(payload, jsonnn)
        r = requests.post(self.url, json=payload, headers=self.headers, auth=(self.user, self.pass_))
        self.requestID += 1
        return (json.loads(r.text))['result']

    def newPayment(self, debitaccountid, amount, currencyid,
                   benefname, benefcountry,
                   extaccountnumber, extbankswift, extbankname, extbenefbankcountry, info):
        doctype = 'Outgoing_Payment_FReq'
        operation = 'NEW'
        payload = {"method": "executeMethod", "id": self.requestID,
                   "params": [self.seshID, {
                       "documenttype": doctype, "id": None, "data": []}, operation]}
        payload['params'][1]['data'].append({"key": "debitaccountid", "value": debitaccountid})
        payload['params'][1]['data'].append({"key": "amount", "value": amount})
        payload['params'][1]['data'].append({"key": "currencyid", "value": currencyid})
        payload['params'][1]['data'].append({"key": "benefname", "value": benefname})
        payload['params'][1]['data'].append({"key": "benefcountry", "value": benefcountry})
        payload['params'][1]['data'].append({"key": "extaccountnumber", "value": extaccountnumber})
        payload['params'][1]['data'].append({"key": "extbankswift", "value": extbankswift.ljust(11, 'X')})
        payload['params'][1]['data'].append({"key": "extbankname", "value": extbankname})
        payload['params'][1]['data'].append({"key": "extbenefbankcountry", "value": extbenefbankcountry})
        payload['params'][1]['data'].append({"key": "info", "value": info})
        print(json.dumps(payload))
        r = requests.post(self.url, json=payload, headers=self.headers, auth=(self.user, self.pass_))
        self.requestID += 1
        return (json.loads(r.text))['result']

    def signPayment(self, id, guid, sig):
        doctype = 'Outgoing_Payment_FReq'
        payload = {"method": "executeMethod",
                   "id": self.requestID,
                   "params": [self.seshID, {
                       "documenttype": doctype,
                       "id": id,
                       "signature": sig
                       # "signature2": sig2
                   }, guid]}
        r = requests.post(self.url, json=payload, headers=self.headers, auth=(self.user, self.pass_))
        self.requestID += 1
        return (json.loads(r.text))

    def placePaymnt(self, debitaccountid, amount, currencyid, benefname, benefcountry, extaccountnumber, extbankswift, extbankname, extbenefbankcountry, info, sig, sig2=''):
        # create doc
        newDoc = self.newPayment(debitaccountid, amount, currencyid,
                                 benefname, benefcountry,
                                 extaccountnumber, extbankswift, extbankname, extbenefbankcountry, info)
        signMeth = next((m for m in newDoc['object']['methods'] if m['caption'] == 'Sign'), None)
        # extract signing requirements
        # e4sign = str(signMeth['signaturetype']) + str(signMeth['signaturetype2'])
        # execute sign method
        self.signPayment(newDoc['objectid'], signMeth['guid'], sig, sig2)

    def placeInternalPayment(self, debitaccid, amount, beneficiary, creditiban, creditaccid, info, signature):
        doctype = 'EP_TRANSFER'
        operation = 'NEW'
        payload = {"method": "executeMethod", "id": self.requestID,
                   "params": [self.seshID, {
                       "documenttype": doctype, "id": None, "data": []}, operation]}
        payload['params'][1]['data'] = [
            {"key": "debitaccountid", "value": debitaccid},
            {"key": "amount", "value": amount},
            {"key": "beneficiary", "value": beneficiary},
            {"key": "myaccount", "value": 0},
            {"key": "creditiban", "value": creditiban},
            {"key": "creditaccountid", "value": creditaccid},
            {"key": "info", "value": info}
        ]
        r = requests.post(self.url, json=payload, headers=self.headers, auth=(self.user, self.pass_))
        self.requestID += 1
        if r.status_code >= 200 and r.status_code <= 201:
            try:
                newDoc = json.loads(r.text)['result']
                signMeth = next((m for m in newDoc['object']['methods'] if m['caption'] == 'Sign'), None)
                if signMeth is not None:
                    print(self.signPayment(newDoc['objectid'], signMeth['guid'], signature))
            except ValueError:
                print('signing doc No_{} failed :('.format(newDoc['objectid']))
        else:
            print(r.text)

    def placeInternalGen(self, n, debitaccid, beneficiary, creditiban, creditaccid, info, signature):
        payloads = []
        for x in range(n):
            doctype = 'EP_TRANSFER'
            operation = 'NEW'
            payload = {"method": "executeMethod", "id": self.requestID,
                       "params": [self.seshID, {
                           "documenttype": doctype, "id": None, "data": []}, operation]}
            payload['params'][1]['data'].append({"key": "debitaccountid", "value": debitaccid})
            payload['params'][1]['data'].append({"key": "amount", "value": random.randrange(1, 10) / 100})
            payload['params'][1]['data'].append({"key": "beneficiary", "value": beneficiary})
            payload['params'][1]['data'].append({"key": "myaccount", "value": 0})
            payload['params'][1]['data'].append({"key": "creditiban", "value": creditiban})
            payload['params'][1]['data'].append({"key": "creditaccountid", "value": creditaccid})
            payload['params'][1]['data'].append({"key": "info", "value": info})

            payloads.append(payload)
            self.requestID += 1
        r = requests.post(self.url, json=payloads, headers=self.headers, auth=(self.user, self.pass_))
        if r.status_code == 200:
            for resultObj in json.loads(r.text):
                signMeth = next((m for m in resultObj['result']['object']['methods'] if m['caption'] == 'Sign'), None)
                if signMeth is not None:
                    try:
                        print(self.signPayment(resultObj['objectid'], signMeth['guid'], signature))
                    except ValueError:
                        print('signing doc No_{} failed :('.format(resultObj['objectid']))
        else:
            print(r.text)




reg_json = {
    "rodne_cislo": "690420/1488",
    "emoney_acc_open": "true",
    "email": "email",
    "password": "Asdfghjkl123456.",
    "salutation": 10,
    "first_name": "Mr",
    "last_name": "Meeseeks",
    "middle_name": "",
    "date_of_birth": "1986-01-01",
    "place_of_birth": "CZE",
    "town_of_birth": "Opatov",
    "gender": 1,
    "id_doc_type": "20",
    "id_doc_number": "123456789",
    "citizenship": "CZE",
    "residence": "CZE",
    "phone": "+420606584858",
    "is_us_person": "false",
    "is_pep": "false",
    "p_address": "8. pěšího pluku 2173",
    "p_city": "Frýdek-Místek",
    "p_zipcode": "73801",
    "p_country": "CZE",
    "is_same_addresses": "true",
    "c_address": "",
    "c_city": "",
    "c_zipcode": "",
    "c_country": "",
    "country_pep": "CZE",
    "occupation_type": 10,
    "occupation_name_of_employer": "FPP Labs",
    "occupation_other": "",
    "aml_est_incoming": 10000,
    "aml_est_outgoing": 10000,
    "aml_est_turnover_in_eur": 2,
    "aml_est_turnover_out_eur": 2,
    "id_doc_file": " data:image/png;base64,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",
    "id_doc2_file": " data:image/png;base64,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",
    "proof_of_addr_file": " data:image/png;base64,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",
    "tos_accept": "true"
}


# 1. Call reg API, read created IDs into memory
# userz = []
# reg_url = 'http://127.0.0.1:8000/registration_api/user/'
# reg_headers = {'Content-type': 'application/json'}
#
# print('Spawner started...')
# for x in tqdm(range(3, 10000)):
#     reg_json['email'] = 'merely@test{}.lol'.format(x)
#     r = requests.post(reg_url, reg_json, reg_headers, auth=('test@test.com', 'Amidala5_'))
#     print(r.text)
# print('Done')

# Step 1.1


userz = []
with open('C:\Fraps\spawned.log') as txt:
    for line in txt:
        if line != ';\n':
            fields = line.strip('\n').split(',')
            userz.append(tuple(fields))

# 2. Create TESTTEST Session, loop through
# 	IBANs in spawned log, sending 2 EUR
def donate_(batch):
    sesh = Session('tester', 'test@test.com', 'Amidala5_', '88.146.252.50')
    for usr in tqdm(batch):
        sesh.placeInternalPayment(3610, 1, 'protege', usr[4], usr[3], 'secret', 'Amidala5_')

#mycode //work on it
def getrightidforsend(usr):
    #need to proseed how to get acutal needeed id
    seshforgetChislo = Session('test',usr[1],usr[2],'127.0.0.1')



donate_(userz[:2])

# batch_size = 100
# procs = []
#
# batches = [userz[i:i + batch_size] for i in range(0, len(userz), batch_size)]
# for index, batch in enumerate(batches):
#     print('Batch No_{} started'.format(index))
#     p = Process(target=donate_, args=(batch,))
#     p.start()
#     procs.append(p)
#
# for p in procs:
#     p.join()
print('done')

# 3. Loop through spawned.log,
# 	logging on and returning 1 EUR back
def return_(usr, pwd):
    sesh = Session('dudoser', usr, pwd, '229.49.4.15')
    sesh.placeInternalGen(99, sesh.getAccounts()[0]['id'], 'monsieur', 'CZ1882700000190000361009',
                          3610, 'donejshen', 'Amidala5_')

def processBatchR(batch):
    j = 0
    start_time = time.time()
    for usr in batch:
        j += 1
        return_(usr[1], usr[2])
        if j == 100:
            print("--- %s seconds ---" % (time.time() - start_time))
            j = 0

batch_size = 1000
procs = []

batches = [userz[i:i + batch_size] for i in range(0, len(userz), batch_size)]
for index, batch in enumerate(batches):
    print('Batch No_{} started'.format(index))
    p = Process(target=processBatchR, args=(batch,))
    p.start()
    procs.append(p)

for p in procs:
    p.join()





# inter = sesh.newInternal(3610, 2, 'pratel', 1, '', 3655, 'comment')

# result = sesh.newPaymentGen(5, 3610, 2, 58, 'CZ698270000000111111111',
#                 'FAPOCZP1', 'fpp', 58)
# print(result)
# curr = sesh.getCurrencies()
# accs = sesh.getAccounts()
# d = sesh.getDocExt(9037)
# print('h')

pass