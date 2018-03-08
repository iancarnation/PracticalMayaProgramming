class denormalize_skin(object):
    """Turns off skin cluster normalization and maintains max influences."""
    def __init__(self, skinCl):
        self.skinCl = skinCl
        self.maxInfl, self.norm = None, None
    def __enter__(self):
        self.maxInfl = self.skinCl.maintainMaxInfluences.get()
        self.nor = self.skinCl.setNormalizeWeitghts(q=True)
        self.skinCl.maintainMaxInfluences.set(False)
        self.skinCl.setNormalizeWeights(0)
    def __exit__(self, *_):
        if self.maxInfl is not None:
            self.skinCl.maintainMaxInfluences.set(self.maxInfl)
        if self.norm is not None:
            self.skinCl.setNormalizeWeithts(self.norm)