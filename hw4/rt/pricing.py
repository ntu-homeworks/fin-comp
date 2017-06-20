class BackwardInduction(object):

    class NodeVariance:
        def __init__(self, h2_t, (i, j), rttree):
            self.h2_t = h2_t
            self.h2_t1 = range(rttree.n * 2 + 1)
            self.suss = range(rttree.n * 2 + 1)

            eta, self.P = rttree.find_eta(h2_t)
            for l in range(-rttree.n, rttree.n + 1):
                self.h2_t1[l] = rttree.rule.h2_t1(l, eta, self.h2_t)
                self.suss[l] = rttree.nodemap[(i+1, j+l*eta)]

    def __init__(self, rttree, strikeprice, variances):
        self.rttree = rttree
        self.strike = strikeprice
        self.k = variances

        self.nodevariances = {}
        self._expand_variances()

    def _expand_variances(self):
        for (i, j), node in self.rttree.nodemap.iteritems():
            base = node.h2min
            step = (node.h2max - node.h2min) / (self.k - 1)

            self.nodevariances[node] = [
                self.NodeVariance(base + step * ki, (i, j), rttree)
                for ki in range(k)
            ]

