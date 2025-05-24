#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
#
# SPDX-License-Identifier: Apache-2.0

import random

def argmin(seq):
    return min(range(len(seq)), key=seq.__getitem__)

def sparse_fisher_yates_iter(n):
    p = dict()
    for i in range(n-1, -1, -1):
        r = random.randrange(i+1)
        yield p.get(r, r)
        if i != r:
            # p[r] = p.pop(i, i) # saves memory, takes time
            p[r] = p.get(i, i) # lazy, but faster


