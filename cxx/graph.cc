
#include <stdio.h>
#include <string.h>
#include <iostream>
#include "graph.h"

using namespace std;

bool loadGraph(const char* fileName, EdgeCollection& edges)
{
    FILE* fh = fopen(fileName, "r");
    if (!fh) {
        printf("Cannot open %s\n", fileName);
        return false;
    }
    char lineBuf[256];
    char *p, *q;
    while (true) {
        if (!fgets(lineBuf, sizeof(lineBuf), fh)) {
            break;
        }
        // strip \n
        lineBuf[strlen(lineBuf) - 1] = 0;
        p = strchr(lineBuf, ',');
        if (!p) {
            continue;
        }
        *p++ = 0;
        unsigned int cost = 1;
        q = strchr(p, ',');
        if (q != nullptr) {
            *q++ = 0;
            cost = atoi(q);
        }
        edges.push_back(Edge(lineBuf, p, cost));
    }
    fclose(fh);
    return true;
}
