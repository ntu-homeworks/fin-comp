from math import log, ceil
from .GRACH import UpdateRule, ProbabilityFactory

class RTTree(object):

    class Node(object):

        def __init__(self, h2, y, n):
            self.h2max = h2
            self.h2min = h2
            self.y = y

            self.pred = []
            self.max_suss = range(2 * n + 1)
            self.min_suss = range(2 * n + 1)

        def add_h2(self, h2):
            self.h2max = max(self.h2max, h2)
            self.h2min = min(self.h2min, h2)

        def __repr__(self):
            return "Node(h2max: %lfe-5, h2min: %lfe-5)" \
                   % (self.h2max * 100000, self.h2min * 100000)

    def __init__(self, days, r, stockprice0, h0, B0, B1, B2, c, periods):
        self.nodemap = {}
        self.y0 = log(stockprice0)
        self.days = days
        self.n = periods
        self.r = r / 365
        self.h0 = h0
        self.gamma = h0
        self.gamma_n = self.gamma / (self.n ** 0.5)

        self.nodemap[(0, 0)] = self.Node(h0 ** 2, self.y0, self.n)
        self.pfactory = ProbabilityFactory(self.gamma, self.n, self.r)
        self.rule = UpdateRule(B0, B1, B2, c, self.gamma_n, self.r)

    def build(self):
        minj, maxj = 0, 0
        for i in range(self.days):
            rng = range(minj, maxj+1)
            minj, maxj = 0, 0

            for j in rng:
                minj, maxj = map(
                    lambda n1, n2, f: f(n1, n2),
                    self._build_suss(i, j), (minj, maxj), (min, max)
                )

    def _build_suss(self, i, j):
        curnode = self.nodemap.get((i, j))
        if curnode == None:
            return 0, 0

        samejump = curnode.h2max == curnode.h2min
        runs = ((curnode.h2max, curnode.max_suss), )
        if not samejump:
            runs += ((curnode.h2min, curnode.min_suss), )

        minj, maxj = 0, 0
        for h2_t, suss in runs:
            eta = int(ceil((h2_t ** 0.5) / self.gamma))

            while True:
                P = self.pfactory(eta, h2_t)
                if P:
                    break
                eta += 1
            minj = min(minj, j - eta * self.n)
            maxj = max(maxj, j + eta * self.n)

            for l in range(-self.n, self.n + 1):
                h2_t1 = self.rule.h2_t1(l, eta, h2_t)

                newsuss = self.nodemap.setdefault(
                    (i+1, j+l*eta),
                    self.Node(h2_t1,
                              curnode.y + self.gamma_n * eta * l,
                              self.n)
                )
                newsuss.add_h2(h2_t1)
                newsuss.pred.append(curnode)

                suss[l] = newsuss

        if samejump:
            curnode.min_suss = curnode.max_suss

        return minj, maxj

