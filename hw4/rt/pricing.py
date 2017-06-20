from math import exp

class BackwardInduction(object):

    class NodeVariance:
        def __init__(self, h2_t, (i, j), rttree):
            self.h2_t = h2_t
            self.h2_t1 = range(rttree.n * 2 + 1)
            self.suss = range(rttree.n * 2 + 1)
            self.price = 0

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
            if i == self.rttree.days:
                continue

            base = node.h2min
            step = (node.h2max - node.h2min) / (self.k - 1)

            self.nodevariances[node] = [
                self.NodeVariance(base + step * ki, (i, j), self.rttree)
                for ki in range(self.k)
            ]

    @property
    def european_callprice(self):
        n = self.rttree.n
        lastdayprice = {node: max(exp(node.y) - self.strike, 0)
                        for node in self.rttree.daynodes[-1]}

        for node in self.rttree.daynodes[-2]:
            for variance in self.nodevariances[node]:
                variance.price = sum(
                    variance.P[l] * lastdayprice[variance.suss[l]]
                    for l in range(-n, n+1)
                )

        for day in self.rttree.daynodes[:-2][::-1]:
            for node in day:
                for variance in self.nodevariances[node]:
                    variance.price = 0

                    for l in range(-n, n+1):
                        suss = variance.suss[l]
                        if variance.h2_t1[l] <= self.nodevariances[suss][0].h2_t:
                            variance.price += variance.P[l] * self.nodevariances[suss][0].price
                            continue

                        for ki in range(self.k):
                            if variance.h2_t1[l] >= self.nodevariances[suss][ki].h2_t:
                                break

                        if ki == self.k - 1:
                            variance.price += variance.P[l] * self.nodevariances[suss][self.k-1].price
                        else:
                            v1 = self.nodevariances[suss][ki]
                            v2 = self.nodevariances[suss][ki+1]
                            variance.price += variance.P[l] * (
                                (variance.h2_t1[l] - v1.h2_t) * v2.price
                                + (v2.h2_t - variance.h2_t1[l]) * v1.price
                            ) / (v2.h2_t - v1.h2_t)

        return self.nodevariances[self.rttree.nodemap[(0, 0)]][0].price
