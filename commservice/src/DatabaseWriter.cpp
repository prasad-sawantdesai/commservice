#include "DatabaseWriter.h"
#include <mongoc.h>
using namespace std;

DatabaseWriter::DatabaseWriter()
{
    //ctor
}

DatabaseWriter::~DatabaseWriter()
{
    //dtor
}
int DatabaseWriter::upload_data(string url, bson_t *doc)
{
    const char *uri_string = url.c_str(); //"mongodb://localhost:27017";
    mongoc_uri_t *uri;
    mongoc_client_t *client;
    mongoc_database_t *database;
    mongoc_collection_t *collection;
    bson_t *command, reply;
    bson_error_t error;
    char *str;
    bool retval;

    mongoc_init ();

    uri = mongoc_uri_new_with_error (uri_string, &error);
    if (!uri)
    {
        fprintf (stderr,
                 "failed to parse URI: %s\n"
                 "error message:       %s\n",
                 uri_string,
                 error.message);
        return EXIT_FAILURE;
    }

    client = mongoc_client_new_from_uri (uri);
    if (!client)
    {
        return EXIT_FAILURE;
    }

    mongoc_client_set_appname (client, "connect-example");

    database = mongoc_client_get_database (client, "x_board");
    collection = mongoc_client_get_collection (client, "x_board", "collection");

    /*
     * Do work. This example pings the database, prints the result as JSON and
     * performs an insert
     */
    command = BCON_NEW ("ping", BCON_INT32 (1));

    retval = mongoc_client_command_simple (
                 client, "admin", command, NULL, &reply, &error);

    if (!retval)
    {
        fprintf (stderr, "%s\n", error.message);
        return EXIT_FAILURE;
    }

    str = bson_as_json (&reply, NULL);
//    printf ("%s\n", str);

    if (!mongoc_collection_insert_one (collection, doc, NULL, NULL, &error))
    {
        fprintf (stderr, "%s\n", error.message);
    }
    bson_destroy (doc);
    bson_destroy (&reply);
    bson_destroy (command);
    bson_free (str);

    /*
     * Release our handles and clean up libmongoc
     */
    mongoc_collection_destroy (collection);
    mongoc_database_destroy (database);
    mongoc_uri_destroy (uri);
    mongoc_client_destroy (client);
    mongoc_cleanup ();


    return 0;
}
