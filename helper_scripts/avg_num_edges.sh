# compute the average number of edges per node in the input contact network (FAVITES format)
cat $1 | cut -f2 | sort -n | uniq -c | rev | cut -d' ' -f2 | rev | numlist -sub1 | numlist -avg
