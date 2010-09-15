
-- Adds all the user info we used to store in LDAP to the User Profile

BEGIN;
CREATE TABLE "mambomsuser_userstatus" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(20) NOT NULL
)
;
INSERT INTO "mambomsuser_userstatus" VALUES 
(1, 'Active'),
(2, 'Pending'),
(3, 'Rejected'),
(4, 'Deleted')
;
ALTER TABLE "mambomsuser_mambomsldapprofile" 
    ADD "title" varchar(50),
    ADD "first_name" varchar(50),
    ADD "last_name" varchar(50),
    ADD "office" varchar(50),
    ADD "office_phone" varchar(50),
    ADD "home_phone" varchar(50),
    ADD "position" varchar(50),
    ADD "department" varchar(50),
    ADD "institute" varchar(50),
    ADD "address" varchar(255),
    ADD "supervisor" varchar(50),
    ADD "area_of_interest" varchar(50),
    ADD "country" varchar(50),
    ADD "node_id" integer REFERENCES "mambomsapp_node" ("id") DEFERRABLE INITIALLY DEFERRED,
    ADD "status_id" integer NOT NULL REFERENCES "mambomsuser_userstatus" ("id") DEFERRABLE INITIALLY DEFERRED DEFAULT 1
;
CREATE INDEX "mambomsuser_mambomsldapprofile_node_id" ON "mambomsuser_mambomsldapprofile" ("node_id");
CREATE INDEX "mambomsuser_mambomsldapprofile_status_id" ON "mambomsuser_mambomsldapprofile" ("status_id");
COMMIT;
