-- Create table for Yak Tenants
CREATE TABLE yak_tenants (
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tenant varchar(100),
    appId varchar(100),
    state varchar(100),
    zone varchar(100),
    cluster varchar(100),
    update_date date
);
-- Create table for Yak Tenants
CREATE TABLE scorpius_tenants (
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    tenant varchar(100),
    appId varchar(100),
    state varchar(100),
    zone varchar(100),
    update_date date
);


-- Create table for App Id, Group and BU mapping
CREATE TABLE appid_group_bu_mapping (
	appId varchar(100) NOT NULL PRIMARY KEY,
    group_fk varchar(100),
    bu varchar(100),
    team_node varchar(100)
);

-- Create table for All Instances from Bastion
CREATE TABLE all_instances_bastion(
	appId varchar(100),
    host_ip varchar(100),
    state varchar(100),
    hostname varchar(100),
    zone varchar(100)
);

-- Temp table which contains all the HBase instances including the ones hosted by Yak
CREATE TABLE active_hbase_including_yak(
	appId varchar(100),
    host_ip varchar(100),
    state varchar(100),
    hostname varchar(100),
    zone varchar(100)
);

