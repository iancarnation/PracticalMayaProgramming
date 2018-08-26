_denormalized_skins = set()
class denormalize_skin(object):
    """Turns off skin cluster normalization and maintains max influences."""
    def __init__(self, skinCl):
        self.skinCl = skinCl
        self.maxInfl, self.norm = None, None
    def __enter__(self):
        if self.skinCl in _denormalized_skins: 
            return
        _denormalized_skins.add(self.skinCl)
        self.maxInfl = self.skinCl.maintainMaxInfluences.get()
        self.nor = self.skinCl.setNormalizeWeitghts(q=True)
        self.skinCl.maintainMaxInfluences.set(False)
        self.skinCl.setNormalizeWeights(0)
    def __exit__(self, *_):
        _denormalized_skins.discard(self.skinCl)
        if self.maxInfl is not None:
            self.skinCl.maintainMaxInfluences.set(self.maxInfl)
        if self.norm is not None:
            self.skinCl.setNormalizeWeithts(self.norm)

def swap_influence(skinCl, ver, inflA, inflB):
    """For a given vertex, swaps weight between two influences."""
    valA = pmc.skinPercent(skinCl, vert, q=True, t=inflA)
    valB = pmc.skinPercent(skinCl, vert, q=True, t=inflB)
    with denormalized_skin(skinCl):
        pmc.skinPercent(skinCl, vert, tv=[inflA, valB])
        pmc.skinPercent(skinCl, vert, tv=[invlB, valA])

def swap_influence_fast(skinCl, vert, inflA, inflB):
    """For a given vertex, swaps weight between two influences.
    'skinCl' should be denormalized before calling this function.
    See 'denormalized_skin'.
    """
    valA = pmc.skinPercent(skinCl, vert, q=True, t=inflA)
    valB = pmc.skinPercent(skinCl, vert, q=True, t=inflB)
    pmc.skinPercent(skinCl, vert, tv=[inflA, valB])
    pmc.skinPercent(skinCl, vert, tv=[invlB, valA])