#!/usr/bin/perl

use strict;
use warnings;
use Data::Dumper;
use File::Basename;

#for i in `ls *.txt` ; do grep -h -A 1 "Page Exist" $i | paste - - - | sed -e "s/^/$i /"  ; done | awk '{ print $1, $4, $5 }' | sed 's/,$/\//'
     
my $filename = $ARGV[0] ;
my @a1; 
my @a2;
my @a3 ;
my @words ;
my @words1 ;
my $recCount = 0 ;
my %counts;

open(my $fh, '<:encoding(UTF-8)', $filename)
	or die "Could not open file '$filename' $!";
     
while (my $row = <$fh>) {
	chomp $row;
	@words = split / /, $row;
	$a1[$recCount] = $words[0] ;
	$words[1] =~ s|/$|| ;
	$words[1] =~ s/https/http/ ;
	$words[2] =~ s/https/http/ ;
	$words[2] =~ s|/$|| ;
	$a2[$recCount] = $words[1] ;
	$a3[$recCount] = $words[2] ;
	$counts{$words[0]}++ ;
	$recCount ++ ;
}

#print "Records read $recCount\n" ;

# get a unique list of file names 
#print Dumper(\%counts);

my @unique = keys(%counts);
my $ucount = @unique ;

#print "Count is $ucount\n" ;

my $i ;
my $k ;
my $j ;

#print "HIJACKS\n" ;
#for ( $i = 0 ; $i < $ucount ; $i++ ) {
	#print "$i $unique[$i] \n" ;
	#for ( $k = 0 ; $k < $recCount ; $k++ ) {
		#if ( $a1[$k] eq $unique[$i] ) {
			#for ( $j = 0 ; $j < $recCount ; $j++ ) {
				#if ( $a1[$j] ne $unique[$i] ) {
					#if ( $a3[$k] eq $a2[$j] ) {
						#@words = split /\-/, $unique[$i] ;
						#print "$words[1] $words[2]   $a3[$k] -> $a2[$k]  \n\t\t";
						#@words = split /\-/, $a1[$j] ;
						#print " == $words[1] $words[2] $a3[$j] -> $a2[$j]\n";
					#}
				#}
			#}
		#}
	#}
#}
#print "Misdirection\n";
for ( $i = 0 ; $i < $ucount ; $i++ ) {
	#print "$i $unique[$i] \n" ;
	for ( $k = 0 ; $k < $recCount ; $k++ ) {
		if ( $a1[$k] eq $unique[$i] ) {
			for ( $j = 0 ; $j < $recCount ; $j++ ) {
				if ( $a1[$j] ne $unique[$i] ) {
					if ( $a2[$k] eq $a2[$j] ) {
						@words = split /\-/, $unique[$i] ;
						#print "$words[1] $words[2]  $a3[$k] -> $a2[$k]  \n\t\t";
						@words = split /\-/, $a1[$j] ;
						#print " == $words[1] $words[2] $a3[$j] -> $a2[$j]\n";
						print "$a3[$j] $a2[$j]\n";
					}
				}
			}
		}
	}
}

