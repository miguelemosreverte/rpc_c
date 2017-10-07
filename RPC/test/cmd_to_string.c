#include <stdio.h>
#include <stdlib.h>

#include <string.h>

char* concatenate(char * dest, char * source) {
    char * out = (char *)malloc(strlen(source) + strlen(dest) + 1);

    if (out != NULL) {
            strcat(out, dest);
            strcat(out, source);
    }

    return out;
}

char * executeCmd(char * cmd) {
    FILE *fp;

    int BUFF_SIZE = 1024;

    int size_line;
    char line[BUFF_SIZE];

    char* results = (char*) malloc(BUFF_SIZE * sizeof(char));

    if (cmd != NULL) {
            /* Open the command for reading. */
            fp = popen(cmd, "r");
            if (fp != NULL) {

            /* Read the output a line at a time - output it. */
            while (fgets(line, size_line = sizeof(line), fp) != NULL) {
                    results = concatenate(results, line);
            }
            }
            /* close */
            pclose(fp);
    } // END if cmd ! null

    return results;
}
