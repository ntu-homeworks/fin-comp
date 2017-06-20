from math import factorial

class UpdateRule(object):

    def __init__(self, B0, B1, B2, c, gamma_n, r):
        self.B0 = B0
        self.B1 = B1
        self.B2 = B2
        self.c = c
        self.gamma_n = gamma_n
        self.r = r

    def h2_t1(self, l, eta, h2_t):
        return self.B0 + self.B1 * h2_t + self.B2 * h2_t * \
               ((self._epsilon_t1(l, eta, h2_t) - self.c) ** 2)

    def _epsilon_t1(self, l, eta, h2_t):
        return (l * eta * self.gamma_n - (self.r - h2_t / 2)) / (h2_t ** 0.5)


class ProbabilityFactory(object):

    class Probability(object):
        def __init__(self, gamma, n, r, eta, h2_t):
            gamma_eta = gamma * eta
            gamma_eta2 = gamma_eta ** 2
            tmp = h2_t / gamma_eta2
            tmp2 = ((r - (h2_t / 2)) / (2 * gamma_eta * (n ** 0.5)))

            self.pu = (tmp / 2) + tmp2
            self.pm = 1 - tmp
            self.pd = (tmp / 2) - tmp2

            self.pl = range(2 * n + 1)
            for ju in range(n + 1):
                for jd in range(n + 1):
                    jm = n - ju - jd
                    l = ju - jd
                    if jm < 0:
                        continue

                    coef = factorial(n) \
                           / (factorial(ju) * factorial(jm) * factorial(jd))
                    self.pl[l] += coef * (self.pu ** ju) \
                                  * (self.pm ** jm) * (self.pd ** jd)

        def truth(self):
            return all(0 <= p <= 1 for p in (self.pu, self.pm, self.pd))

        def __getitem__(self, l):
            return self.pl[l]

    def __init__(self, gamma, n, r):
        self.gamma = gamma
        self.n = n
        self.r = r

    def __call__(self, eta, h2_t):
        return self.Probability(self.gamma, self.n, self.r, eta, h2_t)
