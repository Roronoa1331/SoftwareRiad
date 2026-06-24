// Neo4j graph schema constraints (Section 6.3.1)
// Graph layer: entity nodes and relationship traversal

CREATE CONSTRAINT artifact_uri IF NOT EXISTS
FOR (n:Artifact) REQUIRE n.uri IS UNIQUE;

CREATE CONSTRAINT museum_uri IF NOT EXISTS
FOR (n:Museum) REQUIRE n.uri IS UNIQUE;

CREATE CONSTRAINT dynasty_uri IF NOT EXISTS
FOR (n:Dynasty) REQUIRE n.uri IS UNIQUE;

CREATE CONSTRAINT artist_uri IF NOT EXISTS
FOR (n:Artist) REQUIRE n.uri IS UNIQUE;

CREATE CONSTRAINT location_uri IF NOT EXISTS
FOR (n:Location) REQUIRE n.uri IS UNIQUE;

CREATE CONSTRAINT material_uri IF NOT EXISTS
FOR (n:Material) REQUIRE n.uri IS UNIQUE;

CREATE CONSTRAINT artifact_type_uri IF NOT EXISTS
FOR (n:ArtifactType) REQUIRE n.uri IS UNIQUE;

CREATE CONSTRAINT culture_uri IF NOT EXISTS
FOR (n:Culture) REQUIRE n.uri IS UNIQUE;

// Example graph traversal query:
// MATCH (a:Artifact)-[:BELONGS_TO_DYNASTY]->(d:Dynasty)
// WHERE d.name CONTAINS 'Ming'
// RETURN a.name, d.name, a.age;
