from .SerializerFactory import factory


class ObjectSerializer:
  def serialize(self, serializeable, format='JSON'):
    serializer = factory.getSerializer(format)
    serializeable.serialize(serializer)
    
    return serializer.toString()
  
objectSerializer = ObjectSerializer()