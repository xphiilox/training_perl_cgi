#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use Encode ();
use JSON::PP ();

sub render_json {
    my $json = JSON::PP->new->canonical->encode({
        ok => JSON::PP::true,
        path => $ENV{SCRIPT_NAME} || '/api/index.cgi',
        method => $ENV{REQUEST_METHOD} || 'GET',
    });

    return "$json\n";
}

sub main {
    print "Content-Type: application/json; charset=utf-8\n\n";
    print Encode::encode('UTF-8', render_json());
}

main() unless caller;

1;
