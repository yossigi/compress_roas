#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <iterator>
#include <map>
#include <set>

using namespace std;

/*
* Given a line in the BGP data trace, returns the index where its data begins.
*/
int get_line_date_index(const string& line) {
	int i = line.find(":");
	if (i < 0) {
		return -1;
	}
	i++;
	while (isspace(line[i])) {
		i++;
	}
	return i;
}

/*
* Writes a new BGP announcement (asn, prefix) to the file (outfile). It keeps a log of written announcements to discard dups.
*/
void write_entry(string& prefix, string& asn, ofstream& outfile, map<string, set<string> >& written) {
	// first check if we wrote this BGP announcement
	if (written.find(prefix) != written.end()) {
		if (written.at(prefix).find(asn) != written.at(prefix).end()) {
			// we did (must be a dup from another route views sensor), so discard it.
			return;
		}
	} else {
		written.insert(pair<string, set<string> >(prefix, set<string>()));
	}
	// keep track on the prefixes we write
	written.at(prefix).insert(asn);

	// there's no maxlen for announcements, we just specify it to be the prefix len to keep the format
	int maxlen_index = prefix.find("/");
	string maxlen(prefix.substr(maxlen_index + 1));
	// write annoucement to file, discard announcements for /0.
	if (maxlen != string("0")) outfile << prefix << "-" << maxlen << "," << asn << endl;
}

// marks for prefix and AS path entries in the BGP RIB file.
static const string kPrefix("PREFIX: ");
static const string kASPath("ASPATH: ");


/*
* Parses a list of BGP RIB files give in the input, saves the output the the given output file
* we assume the RIB files given by route views (http://www.routeviews.org/), 
* parsed by libbgpdump (see https://bitbucket.org/ripencc/bgpdump/wiki/Home),
* and then fed to this application as input.
*/
int main(int argc, char* argv[]) {
	if (argc < 3) {
		cout << "usage:" << argv[0] << " bgp_rib_files output_file" << endl;
		return 1;
	}
	
	// the output file
	ofstream outfile(argv[argc - 1]);

	// written BGP announcement logs
	map<string, set<string> > written;

	// iterate through the RIB files, parse the announcements in each of them
	for (int file_index = 1; file_index < argc - 1; file_index++) {
		ifstream infile(argv[file_index]);
		cout << "parsing file " << argv[file_index] << endl;
		string line;
		string prefix;
		string asn;

		// read line by line, parse each anonucement
		while (getline(infile, line)) {
			if (line == "\n") {
				prefix.clear();
				asn.clear();
				continue;
			}

			// check if this line specifies an IP prefix
			if (line.find(kPrefix) == 0) {
				int i = get_line_date_index(line);
				// get the prefix
				prefix = line.substr(i);

			// check if this line specifies an AS path
			} else if (line.find(kASPath) == 0) {
				// parse the AS path
				int i = get_line_date_index(line);
				string raw_route = line.substr(i);
				i = raw_route.find(" {");
				string route;
				if (i >= 0) {
					route = raw_route.substr(0, i);
				} else {
					route = raw_route;
				}

				// split the AS path into the ASNs that compose it. Get the origin ASN.
				istringstream iss(route);
				vector<string> tokens;
				copy(istream_iterator<string>(iss),	istream_iterator<string>(), back_inserter(tokens));
				if (tokens.size() > 0) {
					// the origin is the last ASN on the route
					asn = tokens.at(tokens.size() - 1);
				} else {
					continue;
				}
			}

			// if we have both the prefix and origin ASN, write it to file.
			if (prefix.size() && asn.size()) {
				write_entry(prefix, asn, outfile, written);
				prefix.clear();
				asn.clear();
			}
		}
	}
	return 0;
}
