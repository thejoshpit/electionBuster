#!/usr/bin/env Rscript
suppressMessages(library( "igraph" ));
library( "getopt" );
library( "png" ) ;

#get options, using the spec as defined by the enclosed list.
#we read the options from the default: commandArgs(TRUE).
spec = matrix(c( 	'file', 'f', 2, "character",
					'output', 'o', 1, "character",
					'title', 't', 1, "character",
					'date', 'd', 1, "character",
					'race', 'r', 1, "character",
					'help', 'h', 0, "logical"
			), byrow=TRUE, ncol=4);
opt = getopt(spec);

# if help was asked for print a friendly message
# and exit with a non-zero error code
if ( !is.null(opt$help) ) {
	cat(getopt(spec, usage=TRUE));
	quit(status=1);
}

#set some reasonable defaults for the options that are needed,
#but were not specified.
if ( is.null(opt$race    ) ) { opt$race    = 'President'     }
if ( is.null(opt$file    ) ) { opt$file    = 'strong.txt'     }
if ( is.null(opt$output  ) ) { opt$output  = paste( opt$file, ".pdf", sep="" ) }
if ( is.null(opt$title    ) ) { opt$title    = 'Relationship'     }
if ( is.null(opt$date    ) ) {  opt$date    = basename(getwd())     }

write( paste("Input file  :", opt$file), stderr() ) ;
write( paste("Output file :", opt$output), stderr() ) ;
write( paste("      Title :", opt$title), stderr() ) ;
write( paste("      Race  :", opt$race), stderr() ) ;
write( paste("      Date  :", opt$date), stderr() ) ;

dd <- read.table( opt$file ) ;
gg <- graph.data.frame(dd, directed=TRUE) ;
g4s <- simplify( gg, remove.multiple = T, remove.loops = T, 
                 edge.attr.comb=c(weight="sum", type="ignore") ) ;
g5s=delete.vertices(g4s,which(degree(g4s)<1));

img1<-readPNG( paste( "~/electionbuster/graph/", opt$race, ".png", sep="" )) ;
img2<-readPNG( paste( "~/electionbuster/graph/", "ballotbox.png", sep="" )) ;

pdf( opt$output, useDingbats=FALSE, width=11, height=8 ) ;

plot.igraph(g5s, main=paste( opt$title, "\nRace:", opt$race, "\nScan Date:", opt$date ), 
	vertex.shape="none",  vertex.label.cex = .5, edge.arrow.size=.1, 
	layout=layout.fruchterman.reingold) 

rasterImage( img1, 1.4,-1.2,1.9,-.7)
rasterImage( img2,-1.4,-1.2,-1.9,-.7)
#mtext( paste('Scan: ', opt$date, ', Race: ', opt$race), side = 1, cex=1 ) ;
mtext( "ElectionBusters", side=4 ) ;

quit() ;


