from .JSONSerializer import JSONSerializer


class SerializerFactory:
  def __init__(self):
    self._creators = {}
    
  def register_format(self, format, creator):
    self._creators[format] = creator
      
  def getSerializer(self, format):
    creator = self._creators.get(format)
    if not creator:
      raise ValueError(format)
    
    return self._creators[format]()
      
      
    
factory = SerializerFactory()
factory.register_format("JSON", JSONSerializer)