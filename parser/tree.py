class Node:
    def __init__(self, vtype, value, children):
        """
        @param vtype: str
        @param value: <anything>
        @param children: list(Node)
        """
        self.vtype = vtype
        self.value = value
        self.children = children

    # Useful for testing 
    def __eq__(self, other):
        return bool(self.vtype == other.vtype and
                    self.value == other.value and
                    self.children == other.children) # shallow

    # Useful for debugging
    def __str__(self):
        return '[Node: {vtype}, {val}, {kids}]'.format(vtype=self.vtype,
                                                        val=self.value,
                                                        kids=self.children)

