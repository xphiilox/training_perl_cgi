#!/usr/bin/env perl
use strict;
use warnings;
use utf8;
use Encode ();

sub html_escape {
    my ($value) = @_;

    $value =~ s/&/&amp;/g;
    $value =~ s/</&lt;/g;
    $value =~ s/>/&gt;/g;
    $value =~ s/"/&quot;/g;
    $value =~ s/'/&#39;/g;

    return $value;
}

sub render_home {
    my @stats = (
        {label => 'Scripts', value => '3', note => 'Ready to run'},
        {label => 'Tests', value => '2', note => 'Passing target'},
        {label => 'Examples', value => '4', note => 'Perl basics'},
        {label => 'Web App', value => '1', note => 'CGI'},
    );

    my @tasks = (
        {name => 'hello.pl を実行する', state => '完了', time => 'Step 1'},
        {name => 'テストを追加する', state => '準備中', time => 'Step 2'},
        {name => 'CGIページを育てる', state => '次にやる', time => 'Step 3'},
    );

    my $stat_cards = join "\n", map {
        sprintf <<'HTML', map { html_escape($_) } @$_{qw(label value note)};
        <article class="card">
          <div class="label">%s</div>
          <div class="value">%s</div>
          <div class="note">%s</div>
        </article>
HTML
    } @stats;

    my $task_rows = join "\n", map {
        my $class = $_->{state} eq '完了' ? 'ok' : $_->{state} eq '次にやる' ? 'warn' : '';
        sprintf <<'HTML', html_escape($_->{name}), html_escape($class), html_escape($_->{state}), html_escape($_->{time});
            <tr>
              <td>%s</td>
              <td><span class="badge %s">%s</span></td>
              <td>%s</td>
            </tr>
HTML
    } @tasks;

    my $html = read_template(template_path());
    $html =~ s/\{\{STAT_CARDS\}\}/$stat_cards/;
    $html =~ s/\{\{TASK_ROWS\}\}/$task_rows/;

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
    $path =~ s{[^/]+$}{index.html};
    return $path;
}

sub main {
    print "Content-Type: text/html; charset=utf-8\n\n";
    print Encode::encode('UTF-8', render_home());
}

main() unless caller;

1;
