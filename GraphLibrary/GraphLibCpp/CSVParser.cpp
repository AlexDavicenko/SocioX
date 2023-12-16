

#include <iostream>
#include <fstream>
#include <string>
#include <list>
#include "CSVParser.h"

using namespace std;



string trim(string s) {


    int start = 0;
    for (int i = 0; i < s.size(); i++) {
        if (!isspace(s[i])) {
            start = i;
            break;
        }
    }
    int end = 0;
    for (int i = s.size() - 1; i > -1; i--) {
        if (!isspace(s[i])) {
            end = i;
            break;
        }
    }

    return s.substr(start, end - start + 1);



}

list<list<string>> parseCSV(string filename) {



    ifstream file(filename);
    list<list<string>> lines;

    if (file.is_open()) {


        list<string> lineBuffer;
        string line;
        while (getline(file, line)) {

            list<char> wordBuffer;
            for (int i = 0; i < line.size(); i++) {
                if (line[i] == ',') {
                    lineBuffer.push_back(trim(string(wordBuffer.begin(), wordBuffer.end())));
                    wordBuffer.clear();

                }
                else {
                    wordBuffer.push_back(line[i]);
                }
            }

            if (wordBuffer.size() != 0) {
                lineBuffer.push_back(trim(string(wordBuffer.begin(), wordBuffer.end())));
            }
            lines.push_back(lineBuffer);
            lineBuffer.clear();
        }

        file.close();
    }
    else {
        cout << "Unable to open file";
    }

    return lines;

}

void exportCSV(list<list<string>> content, string filename) {


    ofstream file(filename);
    for (const list<string>& line : content) {
        int count = 0;
        for (const string& word : line) {
            if (count == line.size() - 1) {
                file << word << endl;
            }
            else {
                file << word << ", ";
            }
            count++;
        }
    }

    file.close();


}
