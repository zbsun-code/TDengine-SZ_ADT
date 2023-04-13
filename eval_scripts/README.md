# Evaluation demo scripts

This directory contains the basic scripts for evaluation.

## Quick Start

First of all, build TDengine with SZ-ADT.

```bash
cd .. && ./build.sh
```

Make sure that all outputs are in the `debug` folder.

Then, run the insert script.

```bash
./run_insert.sh
```

After running, the script will finally report the messages below:

```
insert test complete!
waiting taosd to stop... 30s
```

And the test report will be written in  `./result_insert.txt`

After finished insert test, you can run query as well:

```bash
./run_query.sh
```

And the test report will be written in  `./result_query.txt`

## Custom evaluation

You can simply edit the file `./insert_syn.json` and `./query_demo.json` to customize your test. Please refer to the taosBenchmark User Manual for details on how to edit most of the arguments.

For query test, we supported random range query with fixed time intervals. You can specify a range query test like this:

```json
{
    ...
    "specified_table_query": {
        "query_interval": 100000,
        "concurrent": 1,
        "sqls": [
            {
                "sql": "select * from xxxx",
                "rand_ts_range": 1,
                "ts_start_ns": 1601510400000000000,
                "ts_end_ns": 1601610399990000000,
                "ts_intv_ns": 500000000000,
                "result": "",
                "ts_precision": "ms"
            }
        ]
    },
    ...
}
```

`rand_ts_range` means enable random range query (1) or not (0). `ts_start_ns` and `ts_end_ns` restricts the largest range of the queries in nanoseconds. `ts_intv_ns` means the time interval of queries. `ts_precision` should be set according to your database configs. Please keep `"result" = ""` in order to avoid the cost of dumping result to files.

## Change TDengine configurations

You can modify TDengine's configurations in `./taosd.cfg`, and arguments related to SZ_ADT evaluation is below:

```
lossyColumns	float|double
entropyType	2       # 0 for original SZ, 2 for SZ_ADT
fPrecision  1E-5    # Error bound in SZ
huffman_force 1     # force compression no matter the size will be smaller or not
```

When testing query performance of TDengine with original SZ, please keep `huffman_force=1`, otherwise the original SZ will bypass the compression due to bad compression ratio during insertion.