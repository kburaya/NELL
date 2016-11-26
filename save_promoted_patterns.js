print("used,precision,string");
db.getCollection('patterns').find({'extracted_category_id':9}).sort({'precision':-1}).forEach(function(pattern){
  print(pattern.used+","+pattern.precision+","+pattern.string);
});