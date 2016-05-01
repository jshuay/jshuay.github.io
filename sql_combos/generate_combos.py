options = [
	#"statistics": [
	[	"analyze table {} delete statistics;",
		"analyze table {} compute statistics;"
	],
	#"inmemory": [
	[	"alter table {} no inmemory;",
		"alter table {} inmemory;"
	],
	#"parallel": [
	[	"alter table {} parallel 1;",
		"alter table {} parallel 4;"
	]
]

tables = [
	"part",
	"supplier",
	"partsupp",
	"customer",
	"orders",
	"lineitem",
	"nation",
	"region"
]
"""
indices = [{
	'lineitem': [
        'drop index l_shipdate_ind;', 
        'create index l_shipdate_ind on lineitem(l_shipdate);'
    ]
}, {
    'customer': [
        'drop index c_mktsegment_ind;',
        'create index c_mktsegment_ind on customer(c_mktsegment);'
    ]
    # We'll want to add more to this one after proof-of-concept...
}, {
    'region': [
        'drop index r_name_ind;',
        'create index r_name_ind on region(r_name);'
    ]
    # We'll want to add more to this one after proof-of-concept...
}, {
	'lineitem': [
        'drop index l_shipdate_ind;',
        'create index l_shipdate_ind on lineitem(l_shipdate);'
    ]
}, {
    'customer': [
        'drop index c_custkey_ind;'
        'create index c_custkey_ind on customer(c_custkey);'
    ]
}, {
    'customer': [
        'drop index c_custkey_ind;'
        'create index c_custkey_ind on customer(c_custkey);'
    ]
}]
"""
# instead, an array for the queries, each which in an array of the on and off
# commands, each for the different indices we want
indices = [
    # query 1
    [
        # off
        [
            'drop index l_shipdate_ind;'
        ],
        # on
        [
            'create index l_shipdate_ind on lineitem(l_shipdate);'
        ]
    ],
    # query 2
    [
        # off
        [

            'drop index c_mktsegment_ind;',
            'drop index c_custkey_ind;',
            'drop index o_custkey_ind;',
            'drop index l_orderkey_ind;',
            'drop index o_orderkey_ind;',
            'drop index o_orderdate_ind;',
            'drop index l_shipdate_ind;',
            # because of group by
            'drop index o_shippriority_ind;'
        ],
        # on
        [
            'create index c_mktsegment_ind on customer(c_mktsegment);',
            'create index c_custkey_ind on customer(c_custkey);',
            'create index o_custkey_ind on orders(o_custkey);',
            'create index l_orderkey_ind on lineitem(l_orderkey);',
            'create index o_orderkey_ind on orders(o_orderkey);',
            'create index o_orderdate_ind on orders(o_orderdate);',
            'create index l_shipdate_ind on lineitem(l_shipdate);',
            # because of group by
            'create index o_shippriority_ind on orders(o_shippriority);'
        ]
    ],
    # query 3
    [
        # off
        [

            'drop index c_custkey_ind;',
            'drop index o_custkey_ind;',
            'drop index l_orderkey_ind;',
            'drop index o_orderkey_ind;',
            'drop index l_suppkey_ind;',
            'drop index s_suppkey_ind;',
            'drop index c_nationkey_ind;',
            'drop index s_nationkey_ind;',
            'drop index n_nationkey_ind;',
            'drop index n_regionkey_ind;',
            'drop index r_regionkey_ind;',
            'drop index r_name_ind;',
            'drop index o_orderdate_ind;',
            # because of group by
            'drop index n_name_ind;',
        ],
        # on
        [

            'create index c_custkey_ind on customer(c_custkey);',
            'create index o_custkey_ind on orders(o_custkey);',
            'create index l_orderkey_ind on lineitem(l_orderkey);',
            'create index o_orderkey_ind on orders(o_orderkey);',
            'create index l_suppkey_ind on lineitem(l_suppkey);',
            'create index s_suppkey_ind on supplier(s_suppkey);',
            'create index c_nationkey_ind on customer(c_nationkey);',
            'create index s_nationkey_ind on supplier(s_nationkey);',
            'create index n_nationkey_ind on nation(n_nationkey);',
            'create index n_regionkey_ind on nation(n_regionkey);',
            'create index r_regionkey_ind on region(r_regionkey);',
            'create index r_name_ind on region(r_name);',
            'create index o_orderdate_ind on orders(o_orderdate);',
            # because of group by
            'create index n_name_ind on nation(n_name);'
        ]
    ],
    # query 4
    [
        # off
        [
            'drop index l_shipdate_ind;',
            'drop index l_discount_ind;',
            'drop index l_quantity_ind;'
        ],
        # on
        [
            'create index l_shipdate_ind on lineitem(l_shipdate);',
            'create index l_discount_ind on lineitem(l_discount);',
            'create index l_quantity_ind on lineitem(l_quantity);'
        ]
    ],
    # query 5
    [
        # off
        [
            ''
        ],
        # on
        [

            'create index  on ();',
            'create index  on ();',
            'create index  on ();',
            'create index  on ();',
            'create index  on ();',
            'create index  on ();',
            # group by
            'create index  on ();',
            'create index  on ();',
            'create index  on ();',
        ]
    ],
    # query 6
    [
        # off
        [
            ''
        ],
        # on
        [
            ''
        ]
    ],
]


def run_sql_file(filename):
    subp = subprocess.Popen(
        ["sudo sqlplus64 system/XxN6uVgdM2PmA67X@localhost:11524/orcl < {}".format(filename)],
        stdout=subprocess.PIPE,
        shell=True)
    return subp.communicate()

import subprocess
states = ['on', 'off']

for query in [6, 18, 22]:

    for mod in ["000", "001", "010", "011", "100", "101", "110", "111"]:
        
        # run modify file modify_###.sql
        modfile = "modify-" + mod + ".sql"
        (o, e) = run_sql_file(modfile)

        for index in range(2):
            indfile = "q{}_index_{}.sql".format(str(query), states[index])
            print indfile
            
            # run query five times:
            fh = open('q{}_m{}_i{}_v{}.csv'.format(str(query), mod, states[index], "off"), 'w')
            for i in range(5):
                subp = subprocess.Popen(["sudo sqlplus64 system/XxN6uVgdM2PmA67X@localhost:11524/orcl < " + "../../hw4/q{}.sql".format(str(query))], stdout=subprocess.PIPE, shell=True)
                (stdout, sterr) = subp.communicate()

                for line in stdout.splitlines():
                    decoded = line.decode()
                    if "Elapsed" in decoded:
                        timesplit = [float(t) for t in decoded.replace(" ", "").split(':')[1:4]]
                        time = (60*60*timesplit[0]) + (60*timesplit[1]) + (timesplit[2])

                        fh.write(str(time) + "\n")                
                        print "Query {}\tIteration {}: {}".format(str(query), str(i), str(time))
            fh.close()


"""
for i in range(0, 2**len(options)):
	if i in [0, 1, 2, 4]:
		continue # we've already done these
	op_lines = []
	bini = "{0:b}".format(i).zfill(len(options)) # "101"
	for b in range(len(bini)):
		for t in tables:
			op_lines.append(options[b][int(bini[b])].format(t))
	with open("modify-" + "{0:b}".format(i).zfill(len(options)) + ".sql", 'w') as fh:
		fh.write("\n".join(op_lines))
"""
