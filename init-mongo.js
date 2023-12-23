instance = new Mongo("mongo_db_node_01:27017");
db = instance.getDB("microblog");

config = {
    "_id": "docker-replicaset",
    "members": [
        {
            "_id": 0,
            "host": "mongo_db_node_01:27017"
        },
        {
            "_id": 1,
            "host": "mongo_db_node_02:27017"
        },
        {
            "_id": 2,
            "host": "mongo_db_node_02:27017"
        }
    ]
};

try {
    rs.conf()
}
catch {
    rs.initiate(config);
}