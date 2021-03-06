#-*- coding: utf8
from __future__ import division, print_function

from prme import mrr

import pandas as pd
import plac
import numpy as np

def main(model, out_fpath):
    store = pd.HDFStore(model)
    
    from_ = store['from_'][0][0]
    to = store['to'][0][0]
    assert from_ == 0
    
    trace_fpath = store['trace_fpath'][0][0]

    XP_hk = store['XP_hk'].values
    XP_ok = store['XP_ok'].values
    XG_ok = store['XG_ok'].values
    alpha = store['alpha'].values[0][0]
    tau = store['tau'].values[0][0]

    hyper2id = dict(store['hyper2id'].values)
    obj2id = dict(store['obj2id'].values)
    
    HSDs = []
    dts = []

    with open(trace_fpath) as trace_file:
        for i, l in enumerate(trace_file): 
            if i < to:
                continue

            dt, h, s, d = l.strip().split('\t')
            if h in hyper2id and s in obj2id and d in obj2id:
                dts.append(float(dt))
                HSDs.append([hyper2id[h], obj2id[s], obj2id[d]])
    
    num_queries = min(10000, len(HSDs))
    queries = np.random.choice(len(HSDs), size=num_queries)
    
    dts = np.array(dts, order='C', dtype='d')
    HSDs = np.array(HSDs, order='C', dtype='i4')
    rrs = mrr.compute(dts, HSDs, XP_hk, XP_ok, XG_ok, alpha, tau)
    
    np.savetxt(out_fpath, rrs)
    store.close()
    
plac.call(main)
