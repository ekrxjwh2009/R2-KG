class Information():
    def __init__(self, qid, claim, gt_entities):
        self.qid = qid
        self.claim = claim
        self.gt_entities = gt_entities
        self.ent_rel_history = []
        # -1 : Abstain_Duplicate (when LLM asks same (ent, rel) pair multiple times)
        # -2 : Abstain_Iteration (when LLM doesn't make inference in given iteration limit)
        # -3 : Abstain_Token (when LLM make token length error)
        # -4 : Regenerate (when exploreKG gives length 0 triples)
        self.state = 1 # 0 : Abstain / Otherwise : Continue
    
    def add_pair(self, addtional_pair):
        self.ent_rel_history.append(addtional_pair)
    
    def set_abstain(self, state):
        self.state = state