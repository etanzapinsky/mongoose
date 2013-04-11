class Node:
    def __init__(self, vtype, inh_value=None, syn_value=None, children=[]):
        """
        @param vtype: str
        @param inh_value: <anything>
        @param syn_value: <anything>
        @param children: list(Node)
        """
        self.vtype = vtype
        self.inh_value = inh_value
        self.syn_value = syn_value
        self.children = children
    
    # Useful for testing 
    def __eq__(self, other):
        if self.children == None:
            return bool(self.vtype == other.vtype and
                        self.inh_value == other.inh_value and
                        self.syn_value == other.syn_value)
        else:
            self_comp = bool(self.vtype == other.vtype and
                        self.inh_value == other.inh_value and
                        self.syn_value == other.syn_value)
            return self_comp and all([self_c == other_c for self_c, other_c in
                                  zip(sorted(self.children), sorted(other.children))])

    # Useful for debugging
    def __str__(self):
        return '[Node: {vtype}, {inh_val}, {syn_val}, {kids}]'.format(vtype=self.vtype,
                                                                      inh_val=self.inh_value,
                                                                      syn_val=self.syn_value,
                                                                      kids=self.children)
