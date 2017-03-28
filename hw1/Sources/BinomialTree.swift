class BinomialTree {

    class Node {
        let price: Money
        weak var upParent: Node? {
            willSet {
                assert(upParent == nil)
            }
        }
        weak var downParent: Node? {
            willSet {
                assert(downParent == nil)
            }
        }
        var downChild: Node? {
            willSet {
                assert(downChild == nil)
            }
        }
        var upChild: Node? {
            willSet {
                assert(upChild == nil)
            }
        }
        var upSibling: Node? {
            return upParent?.upChild
        }
        var downSibling: Node? {
            return downParent?.downChild
        }

        init(price: Money, upParent: Node? = nil, downParent: Node? = nil, downChild: Node? = nil, upChild: Node? = nil) {
            self.price = price
            self.upParent = upParent
            self.downParent = downParent
            self.downChild = downChild
            self.upChild = upChild
        }

        func insert(downChild price: Money) -> Node {
            downChild = Node(price: price, upParent: self)
            return downChild!
        }

        func insert(upChild price: Money) -> Node {
            upChild = Node(price: price, downParent: self)
            return upChild!
        }

        func insert(downExistChild child: Node) -> Node {
            downChild = child
            child.upParent = self
            return downChild!
        }

        func insert(upExistChild child: Node) -> Node {
            upChild = child
            child.downParent = self
            return upChild!
        }
    }

    let root: Node
    var levels: [[Node]]

    init(spotPrice S: Money, upFactor u: Double, downFactor d: Double, numPeriods n: Int) {
        root = Node(price: S)
        levels = [[root]]

        for _ in 0..<n {
            var currentLevel = levels.last!
            levels.append([])
            var childLevel = levels.last!

            childLevel.append(Node(price: currentLevel[0].price * u))

            for currentNode in currentLevel {
                currentNode.insert(upExistChild: childLevel.last!)
                childLevel.append(currentNode.insert(downChild: currentNode.price * d))
            }
        }
    }
}
