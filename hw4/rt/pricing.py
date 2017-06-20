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
        return self._pricing(True, True)

    @property
    def european_putprice(self):
        return self._pricing(False, True)

    @property
    def american_callprice(self):
        return self._pricing(True, False)

    @property
    def american_putprice(self):
        return self._pricing(False, False)

    def _pricing(self, call_put, european_american):
        def profit(p):
            return max((p - self.strike) * (1 if call_put else -1), 0)
        def eraly_term(p):
            return p if european_american else max(p, 0)

        n = self.rttree.n
        lastdayprice = {node: profit(exp(node.y))
                        for node in self.rttree.daynodes[-1]}

        for node in self.rttree.daynodes[-2]:
            for variance in self.nodevariances[node]:
                variance.price = eraly_term(sum(
                    variance.P[l] * lastdayprice[variance.suss[l]]
                    for l in range(-n, n+1)
                ))

        for day in self.rttree.daynodes[:-2][::-1]:
            for node in day:
                for variance in self.nodevariances[node]:
                    variance.price = 0

                    for l in range(-n, n+1):
                        h2_t1 = variance.h2_t1[l]
                        suss = self.nodevariances[variance.suss[l]]

                        if suss[0].h2_t < h2_t1 < suss[-1].h2_t:
                            for ki in range(self.k):
                                if h2_t1 >= suss[ki].h2_t:
                                    break

                            v1 = suss[ki]
                            v2 = suss[ki+1]
                            price = ((h2_t1 - v1.h2_t) * v2.price
                                     + (v2.h2_t - h2_t1) * v1.price
                                    ) / (v2.h2_t - v1.h2_t)

                        else:
                            price = suss[0].price if h2_t1 <= suss[0].h2_t \
                                    else suss[-1].price

                        variance.price += variance.P[l] * price

                    variance.price = eraly_term(variance.price)

        return self.nodevariances[self.rttree.nodemap[(0, 0)]][0].price
