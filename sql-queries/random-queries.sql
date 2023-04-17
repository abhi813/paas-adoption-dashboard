-- Yak tenants list with Group and BU
select y.appId, y.tenant, y.state, y.update_date, y.zone, mapp.appId, mapp.group_fk, mapp.bu
from yak_tenants y
join appid_group_bu_mapping mapp on (y.appId = mapp.appId);

-- Insert into the Temp table which contain HBase + Yak
insert into active_hbase_including_yak (appId, host_ip, state, hostname,  zone)
select appId, host_ip, state, hostname,  zone from all_instances_bastion where state = "active" and hostname like "%hbase%";

-- Yak existing tenants list with Group and BU
select y.tenant, y.state, y.update_date, y.zone, mapp.appId, mapp.group_fk, mapp.bu
from yak_tenants y
join appid_group_bu_mapping mapp on (y.appId = mapp.appId);

-- Yak Universe list with Group and BU
select t1.appId, mapp.group_fk, mapp.bu from 
(select count(*), appId from active_hbase_including_yak where hostname not like "%yak%" group by appId) t1
left join appid_group_bu_mapping mapp on (t1.appId = mapp.appId);

-- Scorpius Tenants list with Group & BU
select y.id, y.tenant, y.state, y.update_date, y.zone, mapp.appId, mapp.group_fk, mapp.bu
from scorpius_tenants y
left join appid_group_bu_mapping mapp on (y.appId = mapp.appId);

-- Redis Universe list with Group & BU
select t1.appId, mapp.group_fk, mapp.bu from 
(select distinct(appId) from all_instances_bastion where state = "active" and hostname like "%redis%") t1
left join appid_group_bu_mapping mapp on (t1.appId = mapp.appId);

-- Couchbase Universe list with Group & BU
select t1.appId, mapp.group_fk, mapp.bu from 
(select distinct(appId) from all_instances_bastion where state = "active" and hostname like "%couchbase%") t1
left join appid_group_bu_mapping mapp on (t1.appId = mapp.appId);

-- Aerospike Universe list with Group & BU
select t1.appId, mapp.group_fk, mapp.bu from 
(select distinct(appId) from all_instances_bastion where state = "active" and hostname like "%aerospike%") t1
left join appid_group_bu_mapping mapp on (t1.appId = mapp.appId);

--------------- SCRATCH PAD AFTER THIS

select count(*), t1.bu, t1.group_fk from
(select y.appId, y.tenant, y.state, y.update_date, y.zone, mapp.group_fk, mapp.bu
from yak_tenants y
join appid_group_bu_mapping mapp on (y.appId = mapp.appId)) t1 group by t1.bu, t1.group_fk;

select count(*), t1.bu, t1.group_fk from
(select y.appId, y.tenant, y.state, y.update_date, y.zone, mapp.group_fk, mapp.bu
from yak_tenants y
join appid_group_bu_mapping mapp on (y.appId = mapp.appId)) t1 group by t1.bu, t1.group_fk;


update scorpius_tenants set zone = "in-chennai-2" where state = "active";

delete from scorpius_tenants where tenant in ("scorpius-global" , "scorpius-template-in-mem");

select * from all_instances_bastion where appId like "%merlin-store_replica%";

select * from appid_group_bu_mapping where appId like "%merlin-store_replica%";