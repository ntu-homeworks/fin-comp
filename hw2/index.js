var ArgumentParser = require('argparse').ArgumentParser;
var Tree = require('./tree.js');

// Parse arguments
var parser = new ArgumentParser({
    description: 'Pricing European-style Asian Single-barrier Up-and-out Calls ' +
                 'Based on the CRR Binomial Tree'
});
parser.addArgument('stockPrice', {
    type: Number,
    help: 'Stock price at time 0',
    metavar: 'S'
});
parser.addArgument('strikePrice', {
    type: Number,
    help: 'Strike price',
    metavar: 'X'
});
parser.addArgument('barrier', {
    type: Number,
    help: 'Barrier, which is higher than S',
    metavar: 'H'
});
parser.addArgument('years', {
    type: Number,
    help: 'Maturity in years',
    metavar: 't'
});
parser.addArgument('volatility', {
    type: Number,
    help: 'Annual volatility (%%)',
    metavar: 'σ'
});
parser.addArgument('r', {
    type: Number,
    help: 'Continuously compounded annual interest rate (%%)'
});
parser.addArgument('numPeriods', {
    type: Number,
    help: 'Number of periods',
    metavar: 'n'
});
parser.addArgument('numStates', {
    type: Number,
    help: 'Number of states per node',
    metavar: 'k'
});

var args = parser.parseArgs();

var tree = new Tree(args);

for (let i=tree.levels.length-1; i>=0; i--) {
    let level = tree.levels[i];

    for (let j=0; j<level.length; j++) {
        let node = level[j];

        for (let state of node.states) {
            if (state.value > args.barrier) {
                // Barrier
                state.callPrice = 0;
                continue;
            }

            if (i == tree.levels.length - 1) {
                // Leaf
                state.callPrice = Math.max(state.value - args.strikePrice, 0);
                continue;
            }

            // Non-leaf
            let cu, cd;
            let au = ((i + 1) * state.value + node.upChild.stockPrice) / (i + 2);
            let ad = ((i + 1) * state.value + node.downChild.stockPrice) / (i + 2);

            let aMaxUp = node.upChild.states[args.numStates].value;
            let aMinUp = node.upChild.states[0].value;
            let aMaxDown = node.downChild.states[args.numStates].value;
            let aMinDown = node.downChild.states[0].value;

            // Interpolate cu
            let l = Math.floor(
                args.numStates * (au - aMinUp) / (aMaxUp - aMinUp)
            );

            if (au >= aMaxUp) {
                cu = node.upChild.states[args.numStates].callPrice;
            } else if (au < aMinUp || !(l >= 0 && l < args.numStates)) {
                cu = node.upChild.states[0].callPrice;
            } else {
                let x = (au - node.upChild.states[l+1].value) / (node.upChild.states[l].value - node.upChild.states[l+1].value);

                if (!(x >= 0 && x <= 1)) {
                    x = 1;
                }

                cu = x * node.upChild.states[l].callPrice +
                    (1 - x) * node.upChild.states[l+1].callPrice;
            }

            // Interpolate cd
            l = Math.floor(
                args.numStates * (ad - aMinDown) / (aMaxDown - aMinDown)
            );

            if (ad >= aMaxDown) {
                cd = node.downChild.states[args.numStates].callPrice;
            } else if (ad < aMinDown || !(l >= 0 && l < args.numStates)) {
                cd = node.downChild.states[0].callPrice;
            } else {
                let x = (ad - node.downChild.states[l+1].value) / (node.downChild.states[l].value - node.downChild.states[l+1].value);

                if (!(x >= 0 && x <= 1)) {
                    x = 1;
                }

                cd = x * node.downChild.states[l].callPrice +
                    (1 - x) * node.downChild.states[l+1].callPrice;
            }

            if (au >= args.barrier)
                cu = 0;
            if (ad >= args.barrier)
                cd = 0;

            state.callPrice = (
                tree.p * cu +
                (1 - tree.p) * cd
            ) / tree.erdt;
        }
    }
}

console.log(tree.root.states[0].callPrice);
