import requests
from bs4 import BeautifulSoup
import json
from bs4.element import Tag

hmaster_host = "hmaster.prod-id-yak-archive-ch2-nn-1"
namenode_host = "namenode.prod-id-yak-archive-ch2-nn-1"

#hmaster_order_hyd_host = "hmaster.prod-id-yak-order-hyd-nn-1"
#namenode_order_hyd_host = "namenode.prod-id-yak-order-hyd-nn-1"

#hmaster_archive_hyd_host = "hmaster.prod-id-yak-archive-hyd-nn-1"
#namenode_archive_hyd_host = "namenode.prod-id-yak-archive-hyd-nn-1"

bastion_api = "http://console.bastion-prod.fkcloud.in/api/user/diagnose"
billing_url = "http://10.47.2.122:28223/ingestion/entities/fkint/fcp/billing/BaseBillingEntity"
cookie = ("session=x9cZTgUUkeRBoJP-26Awlw.d5afqk9rESx82ND2CoYJujtemyC3CpikLhxh8hM2y5qX_ehe3O8PxyYJcxNk7KOiUl4xUNnd0MyGsoQzvQXv37_SfoMaserl4ej7ysFeEJtegB5qazmkahjv89KG7XyVC5C_NDIWzAyBFKP4AJPp81pR6wpgduJAwgn4gPGn4sbPTcXeqbmTQH7i1Px0ewbdbsuYf6IIpQ25GS8SzS1b45mjtupSzRPE7DYJgb77ur7FWl_jBSHJKpxT68zyMHbsvrnL8R7WkyImy557X0XYOXCSkiFR6UUTrHPBWNBvmCSJKc_QBBwUXaE2q_oTRcJ0YrWYcvHA-onfYXSfiT_gGOJ9XLARYFrNGSSLXuVdMYiKIWVV-1cE6Me9BtcmMaeSmKcrc0-tqaBQxY5kvBvnVMRqwe7qjK-uIXqKX04KATadQZmCB86kHv_ROesK9daCdjwbxdYhXMeflYgXhxpFD0fprzXk0294iZQfXJu60K-6yHmT4ewL7P4nmSKUTW6ImcdVhyejvg6zcz47aFhxtH7wvs59JEsAKZc9uXj55-Bl1mijHUYRSY1FUatSTsSls5VoV92hC0sibOyfErahXTuKmugTJ1JM3zgejjR43uman3_NxOyd_HgsmXYZi4I13gUnJM_aukzg-b1Bq8_IgxDQ_vWgzT8M8D7Y15TUz2_RoObC0seoFHuCr3EgVnIGiYCFUY4M1cVUZxVxHOCdp0NOaTWaOWBpcBMCT13ny0OfgF6ABfdKFsXTNl7-oYymho3CLaVmOQKE9Rn37ggFfr6h3UOxXqoFbplFW_a2FAoRhavRs8bjcBpkAyDh1iKJhsVGrBwHj0vwovbiogTH79qyajr1altI_PSOGxbEMbdR5Ify7s-ssEG5ezL1jJ_VTbFTOOUWTaeYRt_x26zdhthm2oUsgMjYljG8k7-opSpVkVpn6MhtFk0o9LQ9b9_ZwQxR_mvkibV3SY1W4dVNr6zJaY72nqBQddVn411Sf4AYolQD2ga8q0EEZnuwil2T4G4aDwwq2LxUUzpajKsJIzyNnxtLNVLZGfC23GgVsSHf021n_iTEFIWBEL3SQMhPlCATRis_Pip0i3tjmaNHmpuK2lKFCuQFq24ST0RhVRAEp4eZjBXL9QDJU3FJ4nq0Q4-kk8KzPS6FyxNiezxXKEifPd5E1KYwIJFXIJ18jM7LdQV5ZWnxMgn6vEdjrj3Hf1grxy1vO4S_iPUac7FhLuHA1zICxT-bCvmbUdHtkZz02Y0yjk5zSQaFb7t6kg7mGZJb81rh3Q-yC2JBkyeivEmfTFmJNduQwj8As6kSv7ulRcTHtobLXDrLpRT-3brLkVw-4vhyFquDLzYxmLMPN19BC7HUw90DnuqLX5ufRUjATKS3lGZp12DMM53jPPlSjdc1UOBJDPWt7cbzGi5DVea-o-YLrqzvRIuipmBlUNcfsqtPSKSTiN-BQv7RM5Y0.1681529941340.1800000.ll6R_H7NEMgYvIa-YmOv60XxowHeIqKmf1wras8y3Z8")
header = {
    "Cookie": cookie,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}
bastion_user = "abhishek.bkumar"
result = {}


def get_cluster_details():
    x = None
    while True:
        x = requests.get('http://' + hmaster_host + '/master-status')
        if x.status_code == 200:
            break
    return x.text


def get_tenant_list(tenants):
    try:
        tenant_list = {}
        for detail in tenants:
            if isinstance(detail, Tag):
                iterablechild = iter(detail.children)
                next(iterablechild)
                data = next(iterablechild).next_element
                regions = 0
                for i in range(10):
                    regions = next(iterablechild).next_element
                if "RSGroup" not in data.string and "default" not in data.string and not data.string.isnumeric():
                    tenant_list[data.string] = int(regions)
        return tenant_list
    except:
        return None

def get_all_tenants(html_data):
    clustersoup = BeautifulSoup(html_data, 'html.parser')
    tables = clustersoup.find_all('table')
    tenant_list = None
    for table in tables:
        tenant_list = get_tenant_list(table)
        if tenant_list is not None:
            break
    return tenant_list
    
    


def get_rsgroup(rsgroup):
    x = None
    while True:
        x = requests.get('http://' + hmaster_host +
                         '/rsgroup.jsp?name=' + rsgroup)
        if x.status_code == 200:
            break
    return x.text


def get_regionservers_of_rsgroup_from_html(html_data):
    rssoup = BeautifulSoup(html_data, 'html.parser')
    tables = rssoup.find_all('table')
    if len(tables) == 0:
        return None
    rsgroup_details = tables[1]
    for detail in rsgroup_details:
        if isinstance(detail, Tag):
            iterablechild = iter(detail.children)
            next(iterablechild)
            data = next(iterablechild).next_element
            regionserver = data.next_element.string.strip()
            if isinstance(data, Tag):
                return regionserver.split(',')
    return None


def get_ip_from_namenode(hostname):
    namenode_response = requests.get(
        "http://"+namenode_host+"/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo")
    if namenode_response.status_code == 200:
        key = hostname+':9866'
        all_nodes = json.loads(json.loads(namenode_response.text)[
                               'beans'][0]['LiveNodes'])
        for node, value in all_nodes.items():
            if node == key:
                return value['infoAddr'].split(':')[0].strip()
        all_dead_nodes = json.loads(json.loads(namenode_response.text)[
                                    'beans'][0]['DeadNodes'])
        for node, value in all_dead_nodes.items():
            if node == key:
                return value['xferaddr'].split(':')[0].strip()
    return None


def get_app_id(ip):
    try:
        api_url = bastion_api.replace('__IP__', ip)
        x = requests.get(api_url, headers=header, params={
            "ip": ip, "user": bastion_user})
        if x.status_code == 200:
            return json.loads(x.text.split('\n')[0].strip()[6:])['appId']
        return ""
    except Exception as ex:
        print(str(ex))
        print(ip)
        return ""

def create_sheet():
    with open('archive-ch2.csv', 'a+') as output:
        for key, value in result.items():
            print(key + " -> " + value)    
            output.write(key + "," + value + "\n")

#User HYD
cluster_details = get_cluster_details()
tenants = get_all_tenants(cluster_details)
for key, value in tenants.items():
    rs_group_data = get_rsgroup(key)
    datanode_hostname = get_regionservers_of_rsgroup_from_html(rs_group_data)
    if datanode_hostname is None:
        continue
    ip = get_ip_from_namenode(datanode_hostname[0])
    app_id = get_app_id(ip) 
    result[key] = app_id

create_sheet()
    
    
