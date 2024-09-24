class Information():
    def __init__(self, qid, claim, gt_entity):
        self.qid = qid
        self.claim = claim
        self.gt_entity = gt_entity # Only one given entity is provided in metaqa
        self.ent_rel_history = []
        self.state = 1 # 0 : Abstain / Otherwise : Continue
    
    def add_pair(self, addtional_pair):
        self.ent_rel_history.append(addtional_pair)
    
    def set_abstain(self):
        self.state = 0