import os, fcntl
from .db import DBConnector
from datetime import datetime

class NodeMap:
    lock_file = None
    map_cols = 'host,cloud,type,account,instance,ip,start'
    
    @staticmethod
    def tsnow():
        return datetime.now().strftime('%s')
    
    @staticmethod
    def history_summary(account, startdate):
        db = DBConnector()
        
        starttime = (datetime.strptime(startdate, "%Y-%m-%d") - datetime(1970, 1, 1)).total_seconds()
        where = "account='%s' and end>'%d'" % (account, int(starttime))
        
        rows = db.select('node_journal', 'type,count(*),sum(end-start)/3600.0 as hours', where = where, group='type')
        data = {row[0]:float(row[2]) for row in rows}
    
        ts_now = int(NodeMap.tsnow())
        rows = db.select('node_map', 'type,sum(%d-start)/3600 as hours' % (ts_now),
                         where = "account='%s' and instance !=''" % (account), group='type')
        
        for row in rows:
            if row[0] not in data:
                data[row[0]] = float(row[1])
            else:
                data[row[0]] += float(row[1])
        
        return data
    
    @staticmethod
    def running_summary(account):
        
        rows = DBConnector().select('node_map', "type,count(*)", where="account='%s' and instance!=''" % (account), group="type")
        return {row[0]:int(row[1]) for row in rows}
        
    def __init__(self):
        self.__lock = None
        self.nodes = {}
        self.cols = NodeMap.map_cols.split(',')
        self.db = DBConnector()
        
        for row in self.db.select('node_map', NodeMap.map_cols):
            node = {self.cols[i]:row[i] for i in range(len(self.cols))}
            self.nodes[node['host']] = node
        
    def lock(self):
        self.__lock = open(self.lock_file, 'w+')
        fcntl.lockf(self.__lock, fcntl.LOCK_EX)
        
    def unlock(self):
        self.__lock.close()
        self.__lock = None
        
    def dump_hosts(self):
        self.lock()
        
        hostsbase_file = os.path.dirname(NodeMap.lock_file) + '/hosts-base'
        with open(hostsbase_file, 'r') as f:
            hostsbase = f.read()
        
        with open('/etc/hosts', 'w') as f:
            f.write(hostsbase + '\n'.join([' '.join(['1.2.3.4' if node['ip']=='' else node['ip'], host]) 
                                           for host, node in self.nodes.items()]) + "\n")
        
        with open('/etc/netgroup', 'w') as f:
            f.write('skyway    ' + ' '.join(['('+ node['ip'] + ',,)' for host, node in self.nodes.items() if node['ip']!='']) + "\n")

        self.unlock()
        return self
        
    def update(self, host, **kwargs):
        for k,v in kwargs.items():
            self.nodes[host][k] = v
        
        self.db.update_one('node_map', 'host', host, kwargs)
        return self
    
    def has_node(self, name):
        return self.nodes[name]['instance'] != ''
        
    def power_on(self, host, instance, ip):
        self.update(host, instance=instance, ip=ip, start=NodeMap.tsnow())
        self.dump_hosts()
    
    def power_off(self, host='', cloud=None, instance=None):
        if (cloud is not None) and (instance is not None):
            for hostname, node in self.nodes.items():
                if node['cloud'] == cloud and node['instance'] == instance:
                    host = hostname
                    break
        
        if host == '' or host not in self.nodes:
            return ''
        
        node = self.nodes[host].copy()
        self.update(host, instance='', ip='', start='0')
        
        node['end'] = NodeMap.tsnow()
        del node['ip']
        self.db.insert_one('node_journal', **node)
        
        self.dump_hosts()
        return node['instance']
    
    def rebuild(self, nodes):
        removed = []
        
        for host,node in self.nodes.items():
            
            if host not in nodes:
                if node['instance']!='':
                    return "Error: failed to rebuild the node map. Node [%s:s] is still on but not in the new node list." % (name, node['instance'])
                
                removed.append(host)
        
        for host in removed:
            del self.nodes[host]
            self.db.remove_one('node_map', 'host', host)
            
        for host in nodes:
            if host not in self.nodes:
                w = host.split("-")
                node = {'host':host, 'cloud':w[1], 'type':w[2], 'account':w[0] + '-' + w[1], 'instance':'', 'ip':'', 'start':0 }
                self.nodes[host] = node
                self.db.insert_one('node_map', **node)
        
        return self
        
        
        
        
        
    
    
