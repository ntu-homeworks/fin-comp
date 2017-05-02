function TreeNode(stockPrice, numStates, aMin, aMax) {
    this.upChild = null;
    this.downChild = null;
    this.upParent = null;
    this.downParent = null;

    this.stockPrice = stockPrice;

    this.states = new Array(numStates + 1);
    for (let m=0; m<=numStates; m++) {
        this.states[m] = {
            value:
                aMin * (numStates - m) / numStates +
                aMax * m / numStates,

            callPrice: null
        };
    }
}

module.exports = TreeNode;
