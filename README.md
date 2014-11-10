
#####
This is a AMQP lib using kombu as idiomatic high-level interface dissociation from openstack component neutron, you 
can use it for second development at any time or any where.
#####

Two faces:
  1> server: you can redefine the Class Manager in the module messager.server for your server-end.        
  2> client: messager.client:ClientProducerAPI can be more efficiency and scalable by yourself.
  3> topic:  help yourself too.
  
High-performance：
  whether the server-end or the client-end, Conntion Pool interface has been reserved to improve the capability, 
  but this function is been disabled default.

Issue:
  1> exchanges and queues can not be clean up when you stop the server-end, may you can resolve this leftover problem
     and tell me the solution， I would appreciate your help.

Detail:
  For more info about this communication libs, looking through the file architecture.txt under dir docs.
  For an introduction to AMQP you should read the article Rabbits and warrens, and the Wikipedia article about AMQP.
