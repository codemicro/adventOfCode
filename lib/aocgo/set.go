package aocgo

type Set []interface{}

func NewSet() *Set {
	return new(Set)
}

func (s *Set) Contains(x interface{}) bool {
	for _, item := range *s {
		if item == x {
			return true
		}
	}
	return false
}

func (s *Set) Add(x interface{}) {
	if !s.Contains(x) {
		*s = append(*s, x)
	}
}

func (s *Set) Union(t *Set) {
	for _, item := range *t {
		s.Add(item)
	}
}

func (s *Set) ShallowCopy() *Set {
	ns := NewSet()
	*ns = append(*ns, *s...)
	return ns
}