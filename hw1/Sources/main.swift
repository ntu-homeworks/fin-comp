import Foundation

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

let u = exp(σ * sqrt(t / Double(n)))
let d = 1 / u

let tree = BinomialTree(spotPrice: S, upFactor: u, downFactor: d, numPeriods: n)
