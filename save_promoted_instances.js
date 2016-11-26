print("used,precision,lexem");
db.getCollection('promoted_instances').find({'category_name':'позвоночное'}).sort({'precision':-1}).forEach(function(instance){
  print(instance.used+","+instance.precision+","+instance.lexem);
});