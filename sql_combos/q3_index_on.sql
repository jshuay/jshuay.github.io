create index c_mktsegment_ind on customer(c_mktsegment);
create index c_custkey_ind on customer(c_custkey);
create index o_custkey_ind on orders(o_custkey);
create index l_orderkey_ind on lineitem(l_orderkey);
create index o_orderkey_ind on orders(o_orderkey);
create index o_orderdate_ind on orders(o_orderdate);
create index l_shipdate_ind on lineitem(l_shipdate);
create index o_shippriority_ind on orders(o_shippriority);
