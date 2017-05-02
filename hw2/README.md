Pricing European-style Asian Single-barrier Up-and-out Calls
============================================================
Based on the CRR binomial tree

梁智湧


## Usage
### Sources
This program is written in [Node.js v7.4.0](https://nodejs.org), which is a popular scripting language framework available on vaious platforms.

Code:

- `index.js`: For main algorithm.
- `tree.js`: For tree data structure and the construction for it.
- `treenode.js`: For the implementation of tree nodes that contain states.

Package decription file:

- `package.json`: For the dependency of this program.

### Run the Program
Node.js is required.

```bash
$ npm install
$ node index.js S X H t σ r n k
```

For detail usage, please use the following command:

```bash
$ node index.js -h
```

#### Example Output

```bash
$ node index.js 100 90 110 1 30 5 120 200
2.997592717082993
```
