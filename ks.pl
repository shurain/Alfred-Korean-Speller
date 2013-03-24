use WebService::KoreanSpeller;
use strict;
use warnings;
use open qw(:std :utf8);
use Unicode::Normalize;


my $NFC_data = "";
while(<>){
    $_ = NFD($_);
    $NFC_data = $NFC_data . "$_";
}
my $data = NFC($NFC_data);

my $checker = WebService::KoreanSpeller->new( text=> $data );
my @results = $checker->spellcheck;   # returns array of hashes
binmode STDOUT, ':encoding(UTF-8)';
foreach my $item (@results) {
    #print $item->{position}, "\n";    # index in the original text (starting from 0)
    print $item->{incorrect}, " -> "; # incorrect spelling
    print $item->{correct}, "\n";     # correct spelling
    #print $item->{comment}, "\n";     # comment about spelling
    #print "------------------------------\n";
}
