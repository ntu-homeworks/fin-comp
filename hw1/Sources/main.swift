import Glibc

typealias Money = Double

let argv = CommandLine.arguments
if argv.count != 7 {
    print("Usage: \(argv[0]) <S: spot price> <K: strike price> <r: risk-free interest rate> <σ: volatility> <T: year> <n: number of periods>")
    exit(1)
}

let S = Money(argv[1])!
let K = Money(argv[2])!
let r = Double(argv[3])!
let σ = Double(argv[4])!
let t = Double(argv[5])!
let n = Int(argv[6])!

let dt = t / Double(n)
let u = exp(σ * sqrt(dt))
let d = 1 / u
let p = (exp(r * dt) - d) / (u - d)

let tree = BinomialTree(spotPrice: S, upFactor: u, downFactor: d, numPeriods: n)

tree.reversedLevelTraverse { (levelNodes: [BinomialTree.Node]) in
    for node in levelNodes {
        assert(node.value == nil)

        let binomialValue = node.upChild != nil ? (exp(-r * dt) * (p * node.upChild!.value! + (1 - p) * node.downChild!.value!)) : 0.0
        let exerciseValue = K - node.price

        node.value = max(binomialValue, exerciseValue)
    }
}

let firstChildren = [tree.root.upChild!, tree.root.downChild!]

let putPrice = tree.root.value!
let Δ = (firstChildren[0].value! - firstChildren[1].value!) / (firstChildren[0].price - firstChildren[1].price)

print("American put price:", putPrice)
print("Delta for the put:", Δ)
