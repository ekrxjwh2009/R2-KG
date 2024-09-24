class Information():
    def __init__(self, qid, claim, gt_entities):
        self.qid = qid
        self.claim = claim
        self.gt_entities = gt_entities
        self.ent_rel_history = []
        self.state = 1 # 0 : Abstain / Otherwise : Continue
    
    def add_pair(self, addtional_pair):
        self.ent_rel_history.append(addtional_pair)
    
    def set_abstain(self):
        self.state = 0