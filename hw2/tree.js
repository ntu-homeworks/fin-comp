var TreeNode = require('./treenode.js');

function Tree(params) {
    this.params = params;

    // Calculate u, d
    let dt = this.params.years / this.params.numPeriods;
    this.u = Math.exp(this.params.volatility / 100 * Math.sqrt(dt));
    this.d = 1 / this.u;
    this.p = (Math.exp(this.params.r / 100 * dt) - this.d) / (this.u - this.d);
    this.erdt = Math.exp(this.params.r / 100 * dt);

    // Define aMax, aMin
    this.aMin = function(i, j) {
        return this.params.stockPrice * (
            (1 - Math.pow(this.d, j+1)) / (1 - this.d) +
            Math.pow(this.d, j) * this.u * (1 - Math.pow(this.u, i-j)) / (1 - this.u)
        ) / (i+1);
    };

    this.aMax = function(i, j) {
        return this.params.stockPrice * (
            (1 - Math.pow(this.u, i-j+1)) / (1 - this.u) +
            Math.pow(this.u, i-j) * this.d * (1 - Math.pow(this.d, j)) / (1 - this.d)
        ) / (i+1);
    };

    // Build tree
    this.root = new TreeNode(
        this.params.stockPrice,
        this.params.numStates,
        this.params.stockPrice,
        this.params.stockPrice
    );

    this.levels = new Array(this.params.numPeriods);
    this.levels[0] = [this.root];

    for (let i=0; i<this.params.numPeriods; i++) {
        let currentLevel = this.levels[i];

        this.levels[i+1] = [new TreeNode(
            currentLevel[0].stockPrice * this.u,
            this.params.numStates,
            this.aMin(i+1, 0),
            this.aMax(i+1, 0)
        )];
        let childLevel = this.levels[i+1];

        for (let j=0; j<currentLevel.length; j++) {
            let currentNode = currentLevel[j];
            let upChildNode = childLevel[j];
            currentNode.upChild = upChildNode;
            upChildNode.downParent = currentNode;

            let downChildNode = new TreeNode(
                currentNode.stockPrice * this.d,
                this.params.numStates,
                this.aMin(i+1, j+1),
                this.aMax(i+1, j+1)
            );
            childLevel.push(downChildNode);
            currentNode.downChild = downChildNode;
            downChildNode.upParent = currentNode;
        }
    }
}

module.exports = Tree;
