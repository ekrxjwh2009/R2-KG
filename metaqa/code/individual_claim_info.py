class Information():
    def __init__(self, qid, claim, gt_entity):
        self.qid = qid
        self.claim = claim
        self.gt_entity = gt_entity # Only one given entity is provided in metaqa
        self.ent_rel_history = []
        # -1 : Abstain_Duplicate (when LLM asks same (ent, rel) pair multiple times)
        # -2 : Abstain_Iteration (when LLM doesn't make inference in given iteration limit)
        # -3 : Abstain_Token (when LLM make token length error)
        # -4 : Regenerate (when exploreKG gives length 0 triples)
        self.state = 1 # Refer to upper abstain condition
    
    def add_pair(self, addtional_pair):
        self.ent_rel_history.append(addtional_pair)
    
    def set_abstain(self, state):
        self.state = state