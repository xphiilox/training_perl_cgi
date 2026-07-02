#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use Encode ();
use JSON::PP ();

# my $cgi = CGI->new;
# my $name = $cgi->param('name');
print "Content-Type: application/json; charset=utf-8\n\n";
print "OK\n";

1;
