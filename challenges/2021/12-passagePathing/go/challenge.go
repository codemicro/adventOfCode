package challenge

import (
	"strings"

	"github.com/codemicro/adventOfCode/lib/aocgo"
)

type node struct {
	isSmall bool
	name    string
}

func newNode(x string) *node {
	return &node{
		isSmall: x == strings.ToLower(x),
		name:    x,
	}
}

type graph struct {
	nodes map[string]*node
	edges map[*node][]*node
}

func newGraph() *graph {
	return &graph{
		nodes: make(map[string]*node),
		edges: make(map[*node][]*node),
	}
}

func parse(instr string) *graph {

	g := newGraph()

	for _, line := range strings.Split(strings.TrimSpace(instr), "\n") {
		sp := strings.Split(line, "-")
		from := sp[0]
		to := sp[1]

		fromNode := g.nodes[from]
		toNode := g.nodes[to]

		if fromNode == nil {
			fromNode = newNode(from)
			g.nodes[from] = fromNode
		}

		if toNode == nil {
			toNode = newNode(to)
			g.nodes[to] = toNode
		}

		g.edges[fromNode] = append(g.edges[fromNode], toNode)
		g.edges[toNode] = append(g.edges[toNode], fromNode)
	}

	return g
}

func countRoutesA(cave *graph, fromNode *node, visited *aocgo.Set) int {
	if fromNode.name == "end" {
		return 1
	}
	var total int
	for _, nextNode := range cave.edges[fromNode] {
		if visited.Contains(nextNode) || nextNode.name == "start" {
			continue
		}

		s := visited.ShallowCopy()
		if fromNode.isSmall {
			s.Add(fromNode)
		}

		total += countRoutesA(cave, nextNode, s)
	}
	return total
}

func countRoutesB(cave *graph, fromNode *node, visited *aocgo.Set, extraUsed bool) int {
	if fromNode.name == "end" {
		return 1
	}
	var total int
	for _, nextNode := range cave.edges[fromNode] {
		if nextNode.name == "start" {
			continue
		}

		var y bool
		if x := visited.Contains(nextNode); x && extraUsed {
			continue
		} else if x {
			y = true
		} else {
			y = extraUsed
		}

		s := visited.ShallowCopy()
		if fromNode.isSmall {
			s.Add(fromNode)
		}

		total += countRoutesB(cave, nextNode, s, y)
	}
	return total
}

type Challenge struct {
	aocgo.BaseChallenge
}

func (c Challenge) One(instr string) (interface{}, error) {
	cave := parse(instr)
	return countRoutesA(cave, cave.nodes["start"], aocgo.NewSet()), nil
}

func (c Challenge) Two(instr string) (interface{}, error) {
	cave := parse(instr)
	return countRoutesB(cave, cave.nodes["start"], aocgo.NewSet(), false), nil
}
