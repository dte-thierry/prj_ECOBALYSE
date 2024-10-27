// -------------------------------------------------------------------
// Pour voir les documents de la collection mycollection, dans MongoDB
// -------------------------------------------------------------------
// > use mydatabase
// switched to db mydatabase
// > show collections
// mycollection
// > db.mycollection.find().pretty()
// {
//         "_id" : ObjectId("671e69353ae24af4e888a35a"),
//         "name" : "Document 1",
//         "value" : 1
// }
// {
//         "_id" : ObjectId("671e69353ae24af4e888a35b"),
//         "name" : "Document 2",
//         "value" : 2
// }
// {
//         "_id" : ObjectId("671e69353ae24af4e888a35c"),
//         "name" : "Document 3",
//         "value" : 3
// }

db = db.getSiblingDB('mydatabase'); // Crée ou sélectionne la base de données 'mydatabase'

db.createCollection('mycollection'); // Crée la collection 'mycollection'

db.mycollection.insertMany([
  { name: "Document 1", value: 1 },
  { name: "Document 2", value: 2 },
  { name: "Document 3", value: 3 }
]); // Insère des documents dans la collection 'mycollection'


// Sélectionner ou créer la base de données 'ecobalyse'
db = db.getSiblingDB('ecobalyse');

// Créer la collection 'textiles'
db.createCollection('textiles');
