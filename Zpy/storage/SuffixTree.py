class SuffixTree:
    """
        Suffix tree
        https://en.wikipedia.org/wiki/Suffix_tree
    """
    def __init__(self, nodes):
        self.root = {"EOW":False, "next": {} }
        for node in nodes:
            self.addNode(node['word'], node['leaf_data'])
    def addNode(self,word, leaf_data):
        """
        Add node to char
        :param word: word
        :param leaf_data: Leaf data
        :return: None
        >>> st = SuffixTree([])
        >>> st.addNode('abc','1M$')
        >>> st.addNode('qwe', '2M$')
        >>> st.addNode('abd', '3M$')
        >>> st.root['next']['a']['next']['b']['next']['c']['EOW']
        '1M$'
        >>> st.root['next']['a']['next']['b']['next']['d']['EOW']
        '3M$'
        >>> 'c' in st.root['next']['a']['next']['b']['next'] and 'd' in st.root['next']['a']['next']['b']['next']
        True
        >>> 'q' not in st.root['next']['q']['next']['w']['next']
        True
        """
        node = self.root
        for ch in word:
            if ch not in node['next']:
                node['next'] [ch] = {"EOW":False, "next": {} }
            node = node['next'][ch]
        node['EOW'] = leaf_data

    def find(self, word):
        """
        Find subword in tree (substring)
        :param word: Keyword in tree
        :return: Leaf data if exist else False
        >>> st = SuffixTree([{'word':'Peppa','leaf_data':'PIG'}, {'word':'Mike', 'leaf_data':'Pro'}, \
                            {'word':'Peppa','leaf_data':'OVERRITE'}])
        >>> st.find('Peppa')
        'OVERRITE'
        >>> st.find('Mike john')
        'Pro'
        >>> st.find('Mikeing')
        False
        """
        node = self.root
        for index, ch in enumerate(word):
            if ch not in node['next']:
                return False
            node = node['next'][ch]
            if node['EOW'] and (index + 1 == len(word) or word[index + 1] == " "):
                return node['EOW']
        return False
