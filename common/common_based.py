class CommonBased(object):
  def __init__(self):
    self.name = None
    self.to_print = []
    self.must_print = []
    self.leader_str = ''
    self.join_char = [',', ',', ',']

  def __str__(self):
    out = []
    for mbp in self.must_print:
      if mbp not in self.to_print:
        self.to_print.append(mbp)
    for attr in self.to_print:
      key = None
      if attr.count(':'):
        attr, key = attr.split(":")
      if attr == 'size' and not getattr(self, 'size_solved', None):
        continue
      if attr == 'discriminant' and not getattr(self, 'discriminant', None):
        continue
      attr_v = getattr(self, attr, None)
      if isinstance(attr_v, (list, set, tuple)):
        out.append("%s: [%s]" % (attr, self.join_char[0].join(map(str, attr_v))))
      elif isinstance(attr_v, dict):
        keys = attr_v.keys()
        if key:
          keys = getattr(self, key, None)
          if not keys or len(key) != len(attr_v.keys()):
            keys = attr_v.keys()
        out.append("%s:\n{%s}" % (attr, self.join_char[1].join(map(lambda x: "%s: %s" % (x, attr_v[x]), keys))))
      else:
        out.append("%s: %s" % (attr, attr_v))
    return "%s{%s}" % (self.leader_str, self.join_char[2].join(out))

  def print(self):
    print(self)

  def update_leader_str(self):
    pass

  def set_name(self, name):
    self.name = name.upper()