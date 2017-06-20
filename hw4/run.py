# -*- coding: utf-8 -*-

import argparse
from pprint import pprint
from rt.tree import RTTree

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Pricing American put options '
                    'based on Ritchken-Trevor algorithm.'
    )
    parser.add_argument('days', metavar='E', type=int,
                        help='days before expiration')
    parser.add_argument('r', type=float, help='annual interest rate')
    parser.add_argument('stockprice', metavar='S', type=float,
                        help='stock price at time 0')
    parser.add_argument('h0', type=float)
    parser.add_argument('B0', metavar='β0', type=float)
    parser.add_argument('B1', metavar='β1', type=float)
    parser.add_argument('B2', metavar='β2', type=float)
    parser.add_argument('c', metavar='c', type=float)
    parser.add_argument('strikeprice', metavar='X', type=float,
                        help='strike price')
    parser.add_argument('periods', metavar='n1', type=int,
                        help='number of partitions per day')
    parser.add_argument('variances', metavar='n2', type=int,
                        help='number of variances per node')

    args = parser.parse_args()

    rttree = RTTree(args.days, args.r, args.stockprice, args.h0,
                    args.B0, args.B1, args.B2, args.c, args.periods)
    rttree.build()
    pprint(rttree.nodemap)
