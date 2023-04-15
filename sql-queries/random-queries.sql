-- Yak tenants list with Group and BU
select y.appId, y.tenant, y.state, y.update_date, y.zone, mapp.appId, mapp.group_fk, mapp.bu
from yak_tenants y
join appid_group_bu_mapping mapp on (y.appId = mapp.appId);

-- Insert into the Temp table which contain HBase + Yak
insert into active_hbase_including_yak (appId, host_ip, state, hostname,  zone)
select appId, host_ip, state, hostname,  zone from all_instances_bastion where state = "active" and hostname like "%hbase%";

select count(*), t1.bu, t1.group_fk from
(select y.appId, y.tenant, y.state, y.update_date, y.zone, mapp.group_fk, mapp.bu
from yak_tenants y
join appid_group_bu_mapping mapp on (y.appId = mapp.appId)) t1 group by t1.bu, t1.group_fk;

select * from yak_tenants;

select * from scorpius_tenants;

delete from scorpius_tenants;

select * from all_instances_bastion where appId like "%merlin-store_replica%";

select * from appid_group_bu_mapping where appId like "%merlin-store_replica%";

CREATE TABLE active_hbase_including_yak(
	appId varchar(100),
    host_ip varchar(100),
    state varchar(100),
    hostname varchar(100),
    zone varchar(100)
);

select * from active_hbase_including_yak order by appId ;

select count(*), appId from active_hbase_including_yak group by appId;

select * from active_hbase_including_yak where hostname not like "%yak%" order by appId;

select count(*), appId from active_hbase_including_yak where hostname not like "%yak%" group by appId;

select count(*) from all_instances_bastion where state = "active" and hostname like "%hbase%";


insert into active_hbase_including_yak (appId, host_ip, state, hostname,  zone)
select appId, host_ip, state, hostname,  zone from all_instances_bastion where state = "active" and hostname like "%hbase%";

select t1.appId, mapp.group_fk, mapp.bu from 
(select count(*), appId from active_hbase_including_yak where hostname not like "%yak%" group by appId) t1
join appid_group_bu_mapping mapp on (t1.appId = mapp.appId);