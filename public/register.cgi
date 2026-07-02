#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use CGI ();
use DBI ();
use Encode ();

sub html_escape {
    my ($value) = @_;
    $value = '' unless defined $value;

    $value =~ s/&/&amp;/g;
    $value =~ s/</&lt;/g;
    $value =~ s/>/&gt;/g;
    $value =~ s/"/&quot;/g;
    $value =~ s/'/&#39;/g;

    return $value;
}

sub dbh {
    my $host = $ENV{DB_HOST} || 'host.docker.internal';
    my $port = $ENV{DB_PORT} || '5432';
    my $name = $ENV{DB_NAME} || 'training_perl';
    my $user = $ENV{DB_USER} || 'training_perl';
    my $password = defined $ENV{DB_PASSWORD} ? $ENV{DB_PASSWORD} : '';

    my $dsn = "dbi:Pg:dbname=$name;host=$host;port=$port";
    return DBI->connect($dsn, $user, $password, {
        AutoCommit => 1,
        RaiseError => 1,
        PrintError => 0,
        pg_enable_utf8 => 1,
    });
}

sub save_registration {
    my (%registration) = @_;
    my $dbh = dbh();

    $dbh->do(
        'insert into registrations (name, blood_type, address) values (?, ?, ?)',
        undef,
        @registration{qw(name blood_type address)},
    );
}

sub form_value {
    my ($q, $name) = @_;
    my $value = scalar $q->param($name);
    return '' unless defined $value;
    return Encode::is_utf8($value) ? $value : Encode::decode('UTF-8', $value);
}

sub handle_request {
    my ($q) = @_;
    return ({}, undef, undef) unless ($ENV{REQUEST_METHOD} || 'GET') eq 'POST';

    my %registration = (
        name => form_value($q, 'name'),
        blood_type => form_value($q, 'blood_type'),
        address => form_value($q, 'address'),
    );

    for my $key (qw(name blood_type address)) {
        $registration{$key} = '' unless defined $registration{$key};
        $registration{$key} =~ s/\A\s+|\s+\z//g;
    }

    return (\%registration, undef, '未入力の項目があります。')
        if grep { $registration{$_} eq '' } qw(name blood_type address);

    eval { save_registration(%registration) };
    return (\%registration, undef, "登録に失敗しました: $@") if $@;

    return ({}, '登録しました。', undef);
}

sub render_register {
    my (%args) = @_;
    my $values = $args{values} || {};
    my $message = $args{message};
    my $error = $args{error};
    my $name = html_escape($values->{name});
    my $blood_type = $values->{blood_type} || '';
    my $address = html_escape($values->{address});
    my $notice_html = '';

    if (defined $message && $message ne '') {
        $notice_html = sprintf '<p class="notice">%s</p>', html_escape($message);
    } elsif (defined $error && $error ne '') {
        $notice_html = sprintf '<p class="notice error">%s</p>', html_escape($error);
    }

    my %selected = map { $_ => $_ eq $blood_type ? ' selected' : '' } qw(A B O AB);

    my $html = read_template(template_path());

    $html =~ s/\{\{NOTICE\}\}/$notice_html/g;
    $html =~ s/\{\{NAME\}\}/$name/g;
    $html =~ s/\{\{ADDRESS\}\}/$address/g;
    $html =~ s/\{\{SELECTED_A\}\}/$selected{A}/g;
    $html =~ s/\{\{SELECTED_B\}\}/$selected{B}/g;
    $html =~ s/\{\{SELECTED_O\}\}/$selected{O}/g;
    $html =~ s/\{\{SELECTED_AB\}\}/$selected{AB}/g;

    return $html;
}

sub read_template {
    my ($path) = @_;

    open my $fh, '<:encoding(UTF-8)', $path or die "Cannot open template $path: $!";
    local $/;
    return <$fh>;
}

sub template_path {
    my $path = __FILE__;
    $path =~ s{[^/]+$}{register.html};
    return $path;
}

sub main {
    my $q = CGI->new;
    my ($values, $message, $error) = handle_request($q);

    print "Content-Type: text/html; charset=utf-8\n\n";
    print Encode::encode('UTF-8', render_register(
        values => $values,
        message => $message,
        error => $error,
    ));
}

main() unless caller;
1;
