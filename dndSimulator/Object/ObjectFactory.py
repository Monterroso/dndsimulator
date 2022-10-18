class ObjectFactory:
  def __init__(self):
    self._builders = {}
    
  def register_builder(self, builderName, builder):
    self._builders[builderName] = builder
    
  def create(self, objectName, **kwargs):
    builder = self._builders.get(objectName)
    
    if not builder:
      return builder(**kwargs)
    
    raise ValueError(objectName)
      